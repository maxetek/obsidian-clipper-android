package com.obsidian.clipper.core

import com.obsidian.clipper.data.model.Metadata
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.jsoup.select.Elements
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ContentExtractor @Inject constructor() {

    suspend fun extractContent(url: String): ExtractedContent = withContext(Dispatchers.IO) {
        try {
            val document = Jsoup.connect(url)
                .userAgent("Mozilla/5.0 (compatible; ObsidianClipper/1.0)")
                .timeout(10000)
                .get()

            val metadata = extractMetadata(document, url)
            val readableContent = extractReadableContent(document)
            val schemaOrg = extractSchemaOrg(document)

            ExtractedContent(
                url = url,
                title = metadata.title ?: document.title(),
                content = readableContent,
                metadata = metadata.copy(schemaOrg = schemaOrg),
                rawHtml = document.html()
            )
        } catch (e: Exception) {
            ExtractedContent(
                url = url,
                title = "Error loading page",
                content = "Failed to extract content: ${e.message}",
                metadata = Metadata(
                    title = "Error",
                    description = "Failed to load page",
                    siteName = extractDomainFromUrl(url)
                ),
                rawHtml = ""
            )
        }
    }

    private fun extractMetadata(document: Document, url: String): Metadata {
        return Metadata(
            title = extractTitle(document),
            description = extractDescription(document),
            author = extractAuthor(document),
            siteName = extractSiteName(document),
            publishedAt = extractPublishedDate(document),
            featuredImage = extractFeaturedImage(document, url),
            favicon = extractFavicon(document, url),
            wordCount = extractWordCount(document),
            canonical = extractCanonicalUrl(document, url)
        )
    }

    private fun extractTitle(document: Document): String? {
        return document.select("meta[property=og:title]").attr("content").ifBlank { null }
            ?: document.select("meta[name=twitter:title]").attr("content").ifBlank { null }
            ?: document.select("title").text().ifBlank { null }
            ?: document.select("h1").first()?.text()
    }

    private fun extractDescription(document: Document): String? {
        return document.select("meta[property=og:description]").attr("content").ifBlank { null }
            ?: document.select("meta[name=twitter:description]").attr("content").ifBlank { null }
            ?: document.select("meta[name=description]").attr("content").ifBlank { null }
    }

    private fun extractAuthor(document: Document): String? {
        return document.select("meta[name=author]").attr("content").ifBlank { null }
            ?: document.select("meta[property=article:author]").attr("content").ifBlank { null }
            ?: document.select("[rel=author]").text().ifBlank { null }
            ?: document.select(".author").text().ifBlank { null }
    }

    private fun extractSiteName(document: Document): String? {
        return document.select("meta[property=og:site_name]").attr("content").ifBlank { null }
            ?: extractDomainFromUrl(document.baseUri())
    }

    private fun extractPublishedDate(document: Document): String? {
        return document.select("meta[property=article:published_time]").attr("content").ifBlank { null }
            ?: document.select("meta[name=publishdate]").attr("content").ifBlank { null }
            ?: document.select("time[datetime]").attr("datetime").ifBlank { null }
    }

    private fun extractFeaturedImage(document: Document, baseUrl: String): String? {
        val imageUrl = document.select("meta[property=og:image]").attr("content").ifBlank { null }
            ?: document.select("meta[name=twitter:image]").attr("content").ifBlank { null }
            ?: document.select("img").first()?.attr("src")
        return imageUrl?.let { resolveUrl(it, baseUrl) }
    }

    private fun extractFavicon(document: Document, baseUrl: String): String? {
        val faviconUrl = document.select("link[rel~=icon]").attr("href").ifBlank { null }
            ?: document.select("link[rel~=shortcut]").attr("href").ifBlank { null }
            ?: "/favicon.ico"
        return faviconUrl?.let { resolveUrl(it, baseUrl) }
    }

    private fun extractWordCount(document: Document): Int? {
        val text = document.select("body").text()
        return if (text.isNotBlank()) {
            text.split("\\s+".toRegex()).size
        } else null
    }

    private fun extractCanonicalUrl(document: Document, originalUrl: String): String {
        return document.select("link[rel=canonical]").attr("href").ifBlank { originalUrl }
    }

    private fun extractReadableContent(document: Document): String {
        // Implement readability algorithm - simplified version
        val contentSelectors = listOf(
            "article",
            "[role=main]", 
            ".content",
            ".post-content",
            ".entry-content",
            ".article-content",
            "main",
            "#content",
            ".main-content"
        )

        for (selector in contentSelectors) {
            val content = document.select(selector)
            if (content.isNotEmpty() && content.text().length > 200) {
                return cleanContent(content.first()!!)
            }
        }

        // Fallback to body content with cleaning
        return cleanContent(document.body())
    }

    private fun cleanContent(element: Element): String {
        // Remove unwanted elements
        element.select("script, style, nav, header, footer, aside, .advertisement, .ad, .social-share").remove()
        
        // Convert to readable text while preserving some structure
        return element.text()
            .replace("\n\s*\n\s*\n".toRegex(), "\n\n") // Clean up excessive newlines
            .trim()
    }

    private fun extractSchemaOrg(document: Document): Map<String, Any>? {
        val schemaElements = document.select("script[type=application/ld+json]")
        if (schemaElements.isEmpty()) return null

        return try {
            // Simplified schema.org extraction
            val schemaText = schemaElements.first()?.data()
            if (!schemaText.isNullOrBlank()) {
                // Parse JSON-LD here - simplified for now
                mapOf("raw" to schemaText)
            } else null
        } catch (e: Exception) {
            null
        }
    }

    private fun extractDomainFromUrl(url: String): String {
        return try {
            java.net.URL(url).host.removePrefix("www.")
        } catch (e: Exception) {
            url
        }
    }

    private fun resolveUrl(url: String, baseUrl: String): String {
        return when {
            url.startsWith("http") -> url
            url.startsWith("//") -> "https:$url"
            url.startsWith("/") -> {
                val base = java.net.URL(baseUrl)
                "${base.protocol}://${base.host}$url"
            }
            else -> {
                val base = java.net.URL(baseUrl)
                "${base.protocol}://${base.host}${base.path.substringBeforeLast("/")}/$url"
            }
        }
    }
}

data class ExtractedContent(
    val url: String,
    val title: String,
    val content: String,
    val metadata: Metadata,
    val rawHtml: String
)
