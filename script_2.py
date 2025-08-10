# Create complete professional Android project files
professional_files = {
    "MainActivity.kt": '''
package com.obsidian.clipper.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.obsidian.clipper.ui.screens.library.LibraryScreen
import com.obsidian.clipper.ui.screens.settings.SettingsScreen
import com.obsidian.clipper.ui.screens.templates.TemplatesScreen
import com.obsidian.clipper.ui.theme.ObsidianClipperTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        setContent {
            ObsidianClipperTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    ClipperApp()
                }
            }
        }
    }
}

@Composable
fun ClipperApp() {
    val navController = rememberNavController()
    
    NavHost(
        navController = navController,
        startDestination = "library"
    ) {
        composable("library") {
            LibraryScreen(
                onNavigateToSettings = { navController.navigate("settings") },
                onNavigateToTemplates = { navController.navigate("templates") }
            )
        }
        composable("settings") {
            SettingsScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable("templates") {
            TemplatesScreen(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
''',

    "ShareActivity.kt": '''
package com.obsidian.clipper.ui

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import com.obsidian.clipper.data.model.*
import com.obsidian.clipper.ui.screens.share.ShareBottomSheet
import com.obsidian.clipper.ui.screens.share.ShareViewModel
import com.obsidian.clipper.ui.theme.ObsidianClipperTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class ShareActivity : ComponentActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val shareContent = extractShareContent(intent)
        
        setContent {
            ObsidianClipperTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background.copy(alpha = 0.1f)
                ) {
                    var showBottomSheet by remember { mutableStateOf(true) }
                    
                    if (showBottomSheet) {
                        ShareBottomSheet(
                            shareContent = shareContent,
                            onDismiss = { 
                                showBottomSheet = false
                                finish()
                            }
                        )
                    }
                }
            }
        }
    }
    
    private fun extractShareContent(intent: Intent): ShareContent {
        return when (intent.action) {
            Intent.ACTION_SEND -> {
                val text = intent.getStringExtra(Intent.EXTRA_TEXT)
                val subject = intent.getStringExtra(Intent.EXTRA_SUBJECT)
                val type = intent.type
                
                when {
                    text != null && text.startsWith("http") -> {
                        ShareContent(
                            type = ContentType.LINK,
                            url = text,
                            title = subject ?: extractTitleFromUrl(text),
                            sourceApp = intent.component?.packageName ?: "unknown"
                        )
                    }
                    text != null -> {
                        ShareContent(
                            type = ContentType.SNIPPET,
                            selectedText = text,
                            title = subject ?: "Shared Text",
                            sourceApp = intent.component?.packageName ?: "unknown"
                        )
                    }
                    type?.startsWith("image/") == true -> {
                        val uri = intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
                        ShareContent(
                            type = ContentType.MEDIA,
                            mediaUri = uri,
                            title = subject ?: "Shared Image",
                            sourceApp = intent.component?.packageName ?: "unknown"
                        )
                    }
                    else -> {
                        ShareContent(
                            type = ContentType.LINK,
                            url = "",
                            title = "Unknown Content",
                            sourceApp = intent.component?.packageName ?: "unknown"
                        )
                    }
                }
            }
            Intent.ACTION_SEND_MULTIPLE -> {
                val uris = intent.getParcelableArrayListExtra<Uri>(Intent.EXTRA_STREAM)
                ShareContent(
                    type = ContentType.MEDIA,
                    title = "Multiple Files",
                    sourceApp = intent.component?.packageName ?: "unknown",
                    mediaUris = uris
                )
            }
            else -> {
                ShareContent(
                    type = ContentType.LINK,
                    url = "",
                    title = "Unknown",
                    sourceApp = intent.component?.packageName ?: "unknown"
                )
            }
        }
    }
    
    private fun extractTitleFromUrl(url: String): String {
        return try {
            val uri = Uri.parse(url)
            uri.host?.removePrefix("www.") ?: "Shared Link"
        } catch (e: Exception) {
            "Shared Link"
        }
    }
}
''',

    "ClipperDatabase.kt": '''
package com.obsidian.clipper.data.database

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import android.content.Context
import com.obsidian.clipper.data.database.dao.*
import com.obsidian.clipper.data.database.entities.*

@Database(
    entities = [
        ClipEntity::class,
        TemplateEntity::class,
        VaultEntity::class,
        HighlightEntity::class
    ],
    version = 1,
    exportSchema = true
)
@TypeConverters(Converters::class)
abstract class ClipperDatabase : RoomDatabase() {
    
    abstract fun clipDao(): ClipDao
    abstract fun templateDao(): TemplateDao
    abstract fun vaultDao(): VaultDao  
    abstract fun highlightDao(): HighlightDao
    
    companion object {
        const val DATABASE_NAME = "obsidian_clipper_db"
        
        @Volatile
        private var INSTANCE: ClipperDatabase? = null
        
        fun getDatabase(context: Context): ClipperDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    ClipperDatabase::class.java,
                    DATABASE_NAME
                )
                .addCallback(DatabaseCallback())
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
    
    private class DatabaseCallback : RoomDatabase.Callback() {
        // Add any initialization logic here
    }
}
''',

    "ContentExtractor.kt": '''
package com.obsidian.clipper.data.network

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
            .replace("\\n\\s*\\n\\s*\\n".toRegex(), "\\n\\n") // Clean up excessive newlines
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
''',

    "VaultManager.kt": '''
package com.obsidian.clipper.utils

import android.content.Context
import android.net.Uri
import androidx.documentfile.provider.DocumentFile
import com.obsidian.clipper.data.model.*
import com.obsidian.clipper.utils.TemplateEngine.ProcessedTemplate
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class VaultManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    
    suspend fun saveClipToVault(
        vault: Vault,
        processedTemplate: ProcessedTemplate,
        assets: List<AssetFile> = emptyList()
    ): SaveResult = withContext(Dispatchers.IO) {
        try {
            val vaultRoot = DocumentFile.fromTreeUri(context, Uri.parse(vault.uri))
                ?: return@withContext SaveResult.Error("Cannot access vault directory")
            
            // Create folder structure
            val targetFolder = createFolderStructure(vaultRoot, processedTemplate.folder)
            
            // Generate unique filename if file exists
            val filename = generateUniqueFilename(targetFolder, processedTemplate.filename)
            
            // Create markdown file
            val markdownFile = targetFolder.createFile("text/markdown", "$filename.md")
                ?: return@withContext SaveResult.Error("Cannot create markdown file")
            
            // Write content
            val fullContent = processedTemplate.frontmatter + "\\n" + processedTemplate.content
            
            context.contentResolver.openOutputStream(markdownFile.uri)?.use { outputStream ->
                outputStream.write(fullContent.toByteArray())
            } ?: return@withContext SaveResult.Error("Cannot write to markdown file")
            
            // Save assets if any
            val assetPaths = if (assets.isNotEmpty()) {
                saveAssets(targetFolder, filename, assets)
            } else emptyList()
            
            SaveResult.Success(
                SavedClip(
                    markdownPath = markdownFile.uri.toString(),
                    assetPaths = assetPaths,
                    filename = filename
                )
            )
            
        } catch (e: Exception) {
            SaveResult.Error("Failed to save clip: ${e.message}")
        }
    }
    
    private fun createFolderStructure(vaultRoot: DocumentFile, folderPath: String): DocumentFile {
        val pathParts = folderPath.split("/").filter { it.isNotBlank() }
        var currentFolder = vaultRoot
        
        for (part in pathParts) {
            currentFolder = currentFolder.findFile(part) 
                ?: currentFolder.createDirectory(part) 
                ?: throw IOException("Cannot create directory: $part")
        }
        
        return currentFolder
    }
    
    private fun generateUniqueFilename(folder: DocumentFile, baseFilename: String): String {
        var filename = sanitizeFilename(baseFilename)
        var counter = 1
        
        while (folder.findFile("$filename.md") != null) {
            filename = "${sanitizeFilename(baseFilename)}_$counter"
            counter++
        }
        
        return filename
    }
    
    private fun sanitizeFilename(filename: String): String {
        return filename
            .replace(Regex("[<>:\\"\\|\\?\\*]"), "")
            .replace("/", "-")
            .replace("\\\\", "-")
            .trim()
            .take(100)
            .ifBlank { "untitled" }
    }
    
    private suspend fun saveAssets(
        parentFolder: DocumentFile,
        baseFilename: String,
        assets: List<AssetFile>
    ): List<String> = withContext(Dispatchers.IO) {
        val assetFolder = parentFolder.createDirectory("${baseFilename}_assets") 
            ?: return@withContext emptyList()
        
        assets.mapNotNull { asset ->
            try {
                val assetFile = assetFolder.createFile(asset.mimeType, asset.filename)
                    ?: return@mapNotNull null
                
                context.contentResolver.openOutputStream(assetFile.uri)?.use { outputStream ->
                    outputStream.write(asset.data)
                }
                
                assetFile.uri.toString()
            } catch (e: Exception) {
                null
            }
        }
    }
    
    suspend fun createVault(name: String, uri: String, isDefault: Boolean = false): Vault {
        return Vault(
            id = generateVaultId(),
            name = name,
            uri = uri,
            isDefault = isDefault,
            createdAt = System.currentTimeMillis()
        )
    }
    
    suspend fun validateVaultAccess(vault: Vault): Boolean = withContext(Dispatchers.IO) {
        try {
            val vaultRoot = DocumentFile.fromTreeUri(context, Uri.parse(vault.uri))
            vaultRoot?.canWrite() == true
        } catch (e: Exception) {
            false
        }
    }
    
    private fun generateVaultId(): String = java.util.UUID.randomUUID().toString()
}

sealed class SaveResult {
    data class Success(val savedClip: SavedClip) : SaveResult()
    data class Error(val message: String) : SaveResult()
}

data class SavedClip(
    val markdownPath: String,
    val assetPaths: List<String>,
    val filename: String
)

data class AssetFile(
    val filename: String,
    val mimeType: String,
    val data: ByteArray
)
'''
}

print("Professional Android files created!")
for filename in professional_files.keys():
    print(f"- {filename}")

# Save all professional files
for filename, content in professional_files.items():
    with open(filename, 'w') as f:
        f.write(content)

print(f"\nCreated {len(professional_files)} professional Android files")