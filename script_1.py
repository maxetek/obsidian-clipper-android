# Create advanced Android components for Obsidian Clipper
advanced_components = {
    "ShareBottomSheet.kt": '''
package com.obsidian.clipper.ui.screens.share

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.obsidian.clipper.data.model.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ShareBottomSheet(
    shareContent: ShareContent,
    onDismiss: () -> Unit,
    viewModel: ShareViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    
    LaunchedEffect(shareContent) {
        viewModel.initializeWithShare(shareContent)
    }
    
    val sheetState = rememberModalBottomSheetState(
        skipPartiallyExpanded = true
    )
    
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        modifier = Modifier.fillMaxHeight(0.9f)
    ) {
        ShareContent(
            uiState = uiState,
            onTitleChanged = viewModel::updateTitle,
            onVaultChanged = viewModel::updateVault,
            onFolderChanged = viewModel::updateFolder,
            onTagsChanged = viewModel::updateTags,
            onNoteChanged = viewModel::updateNote,
            onTemplateChanged = viewModel::updateTemplate,
            onToggleChanged = viewModel::updateToggle,
            onHighlightAdded = viewModel::addHighlight,
            onSave = { 
                viewModel.saveClip()
                onDismiss()
            },
            onCancel = onDismiss
        )
    }
}

@Composable
private fun ShareContent(
    uiState: ShareUiState,
    onTitleChanged: (String) -> Unit,
    onVaultChanged: (Vault) -> Unit,
    onFolderChanged: (String) -> Unit,
    onTagsChanged: (List<String>) -> Unit,
    onNoteChanged: (String) -> Unit,
    onTemplateChanged: (Template) -> Unit,
    onToggleChanged: (String, Boolean) -> Unit,
    onHighlightAdded: (String) -> Unit,
    onSave: () -> Unit,
    onCancel: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Header
        ShareHeader(
            contentType = uiState.contentType,
            isProcessing = uiState.isProcessing,
            onCancel = onCancel
        )
        
        Divider()
        
        // Title field
        OutlinedTextField(
            value = uiState.title,
            onValueChange = onTitleChanged,
            label = { Text("Title") },
            modifier = Modifier.fillMaxWidth(),
            enabled = !uiState.isProcessing
        )
        
        // Vault and folder selection
        VaultFolderSelector(
            selectedVault = uiState.selectedVault,
            selectedFolder = uiState.selectedFolder,
            availableVaults = uiState.availableVaults,
            availableFolders = uiState.availableFolders,
            onVaultChanged = onVaultChanged,
            onFolderChanged = onFolderChanged,
            enabled = !uiState.isProcessing
        )
        
        // Tags input
        TagsInput(
            tags = uiState.tags,
            onTagsChanged = onTagsChanged,
            suggestedTags = uiState.suggestedTags,
            enabled = !uiState.isProcessing
        )
        
        // Template selector
        if (uiState.availableTemplates.isNotEmpty()) {
            TemplateSelector(
                selectedTemplate = uiState.selectedTemplate,
                availableTemplates = uiState.availableTemplates,
                onTemplateChanged = onTemplateChanged,
                enabled = !uiState.isProcessing
            )
        }
        
        // Notes field
        OutlinedTextField(
            value = uiState.note,
            onValueChange = onNoteChanged,
            label = { Text("Notes") },
            modifier = Modifier.fillMaxWidth(),
            minLines = 2,
            enabled = !uiState.isProcessing
        )
        
        // Processing options
        ProcessingOptionsCard(
            options = uiState.processingOptions,
            onToggleChanged = onToggleChanged,
            enabled = !uiState.isProcessing
        )
        
        // Highlights section (if applicable)
        if (uiState.contentType == ContentType.ARTICLE) {
            HighlightsSection(
                highlights = uiState.highlights,
                onHighlightAdded = onHighlightAdded,
                enabled = !uiState.isProcessing
            )
        }
        
        // Action buttons
        ActionButtons(
            isProcessing = uiState.isProcessing,
            onSave = onSave,
            onCancel = onCancel
        )
        
        // Bottom padding for navigation
        Spacer(modifier = Modifier.height(24.dp))
    }
}

@Composable
private fun ShareHeader(
    contentType: ContentType,
    isProcessing: Boolean,
    onCancel: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Icon(
                imageVector = when(contentType) {
                    ContentType.LINK -> Icons.Default.Link
                    ContentType.ARTICLE -> Icons.Default.Article
                    ContentType.SNIPPET -> Icons.Default.TextSnippet
                    ContentType.MEDIA -> Icons.Default.Image
                },
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary
            )
            Text(
                text = "Clip to Obsidian",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.SemiBold
            )
            if (isProcessing) {
                CircularProgressIndicator(
                    modifier = Modifier.size(16.dp),
                    strokeWidth = 2.dp
                )
            }
        }
        IconButton(onClick = onCancel) {
            Icon(Icons.Default.Close, contentDescription = "Close")
        }
    }
}

@Composable
private fun ProcessingOptionsCard(
    options: Map<String, Boolean>,
    onToggleChanged: (String, Boolean) -> Unit,
    enabled: Boolean
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Processing Options",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold
            )
            
            options.forEach { (option, checked) ->
                ProcessingToggle(
                    text = getOptionDisplayName(option),
                    checked = checked,
                    onCheckedChange = { onToggleChanged(option, it) },
                    enabled = enabled
                )
            }
        }
    }
}

@Composable  
private fun ProcessingToggle(
    text: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    enabled: Boolean
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            enabled = enabled
        )
        Spacer(modifier = Modifier.width(12.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodyMedium,
            color = if (enabled) {
                MaterialTheme.colorScheme.onSurface
            } else {
                MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
            }
        )
    }
}

private fun getOptionDisplayName(option: String): String {
    return when (option) {
        "extractContent" -> "Extract article content"
        "saveMarkdown" -> "Save as Markdown"
        "saveRawHtml" -> "Save raw HTML"
        "downloadAssets" -> "Download assets offline"
        "readItLater" -> "Read it later"
        "favorite" -> "Add to favorites"
        "enableHighlights" -> "Enable highlighting"
        else -> option.replaceFirstChar { it.titlecase() }
    }
}

@Composable
private fun ActionButtons(
    isProcessing: Boolean,
    onSave: () -> Unit,
    onCancel: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Button(
            onClick = onSave,
            modifier = Modifier.weight(1f),
            enabled = !isProcessing
        ) {
            if (isProcessing) {
                CircularProgressIndicator(
                    modifier = Modifier.size(16.dp),
                    strokeWidth = 2.dp,
                    color = MaterialTheme.colorScheme.onPrimary
                )
                Spacer(modifier = Modifier.width(8.dp))
            }
            Text(if (isProcessing) "Saving..." else "Save Clip")
        }
        
        OutlinedButton(
            onClick = onCancel,
            modifier = Modifier.weight(0.3f),
            enabled = !isProcessing
        ) {
            Text("Cancel")
        }
    }
}
''',

    "TemplateEngine.kt": '''
package com.obsidian.clipper.utils

import com.obsidian.clipper.data.model.*
import kotlinx.datetime.*
import java.util.regex.Pattern
import org.jsoup.Jsoup

class TemplateEngine {
    companion object {
        private val VARIABLE_PATTERN = Pattern.compile("\\{\\{([^}]+)\\}\\}")
        private val CONDITIONAL_PATTERN = Pattern.compile("\\{%\\s*if\\s+([^%]+)\\s*%\\}([^{]*?)\\{%\\s*endif\\s*%\\}")
        private val LOOP_PATTERN = Pattern.compile("\\{%\\s*for\\s+(\\w+)\\s+in\\s+(\\w+)\\s*%\\}([^{]*?)\\{%\\s*endfor\\s*%\\}")
    }

    fun processTemplate(
        template: Template,
        clipData: ClipData,
        metadata: Metadata?,
        highlights: List<Highlight> = emptyList()
    ): ProcessedTemplate {
        try {
            val variables = createVariableContext(clipData, metadata, highlights)
            var content = template.content
            
            // Process conditionals first
            content = processConditionals(content, variables)
            
            // Process loops
            content = processLoops(content, variables)
            
            // Process variables
            content = processVariables(content, variables)
            
            // Generate frontmatter
            val frontmatter = generateFrontmatter(clipData, metadata, highlights)
            
            return ProcessedTemplate(
                content = content,
                frontmatter = frontmatter,
                filename = generateFilename(template, clipData, variables),
                folder = determineFolder(template, clipData, variables)
            )
            
        } catch (e: Exception) {
            return ProcessedTemplate(
                content = "Error processing template: ${e.message}\\n\\n${template.content}",
                frontmatter = generateFrontmatter(clipData, metadata, highlights),
                filename = sanitizeFilename(clipData.title),
                folder = "Clips"
            )
        }
    }

    private fun createVariableContext(
        clipData: ClipData,
        metadata: Metadata?,
        highlights: List<Highlight>
    ): Map<String, Any?> {
        val now = Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault())
        
        return mutableMapOf<String, Any?>().apply {
            // Page variables - exact match with browser extension
            put("title", clipData.title.ifBlank { metadata?.title ?: "Untitled" })
            put("url", clipData.url)
            put("domain", clipData.domain)
            put("favicon", metadata?.favicon)
            put("published", metadata?.publishedAt)
            put("author", metadata?.author)
            put("length", metadata?.wordCount)
            put("excerpt", metadata?.description)
            put("site_name", metadata?.siteName)
            put("image", metadata?.featuredImage)
            
            // Content variables
            put("content", clipData.extractedContent)
            put("selection", clipData.selectedText)
            put("note", clipData.note)
            
            // Highlight variables
            put("highlights", highlights)
            put("highlight_count", highlights.size)
            
            // Date variables
            put("date", now.date.toString())
            put("time", now.time.toString())
            put("datetime", now.toString())
            put("timestamp", Clock.System.now().epochSeconds)
            
            // Meta variables
            put("tags", clipData.tags)
            put("tag_list", clipData.tags.joinToString(", "))
            
            // Schema.org variables
            metadata?.schemaOrg?.let { schema ->
                put("schema", schema)
                schema.forEach { (key, value) ->
                    put("schema.$key", value)
                }
            }
        }
    }

    private fun processVariables(content: String, variables: Map<String, Any?>): String {
        val matcher = VARIABLE_PATTERN.matcher(content)
        val result = StringBuffer()
        
        while (matcher.find()) {
            val variableExpression = matcher.group(1)
            val replacement = processVariableExpression(variableExpression, variables)
            matcher.appendReplacement(result, escape(replacement))
        }
        matcher.appendTail(result)
        
        return result.toString()
    }

    private fun processVariableExpression(expression: String, variables: Map<String, Any?>): String {
        val parts = expression.split("|").map { it.trim() }
        val variableName = parts[0]
        val filters = parts.drop(1)
        
        var value = getNestedValue(variableName, variables)
        
        // Apply filters
        for (filter in filters) {
            value = applyFilter(value, filter, variables)
        }
        
        return value?.toString() ?: ""
    }

    private fun getNestedValue(path: String, variables: Map<String, Any?>): Any? {
        val parts = path.split(".")
        var current: Any? = variables
        
        for (part in parts) {
            current = when (current) {
                is Map<*, *> -> current[part]
                is List<*> -> {
                    val index = part.toIntOrNull()
                    if (index != null && index < current.size) current[index] else null
                }
                else -> null
            }
            if (current == null) break
        }
        
        return current
    }

    private fun applyFilter(value: Any?, filter: String, variables: Map<String, Any?>): Any? {
        if (value == null) return null
        
        val filterParts = filter.split(":")
        val filterName = filterParts[0].lowercase()
        val args = filterParts.drop(1)
        
        return when (filterName) {
            "lower" -> value.toString().lowercase()
            "upper" -> value.toString().uppercase()
            "title" -> value.toString().split(" ").joinToString(" ") { 
                it.replaceFirstChar { c -> c.titlecaseChar() } 
            }
            "trim" -> value.toString().trim()
            "truncate" -> {
                val length = args.firstOrNull()?.toIntOrNull() ?: 100
                val text = value.toString()
                if (text.length <= length) text else text.take(length) + "..."
            }
            "replace" -> {
                if (args.size >= 2) {
                    value.toString().replace(args[0], args[1])
                } else value
            }
            "striphtml" -> Jsoup.parse(value.toString()).text()
            "markdown" -> convertToMarkdown(value.toString())
            "date" -> formatDate(value, args.firstOrNull() ?: "yyyy-MM-dd")
            "join" -> {
                val separator = args.firstOrNull() ?: ", "
                when (value) {
                    is List<*> -> value.joinToString(separator)
                    is Array<*> -> value.joinToString(separator)
                    else -> value.toString()
                }
            }
            "first" -> {
                when (value) {
                    is List<*> -> value.firstOrNull()
                    is Array<*> -> value.firstOrNull()
                    else -> value
                }
            }
            "last" -> {
                when (value) {
                    is List<*> -> value.lastOrNull()
                    is Array<*> -> value.lastOrNull()
                    else -> value
                }
            }
            "default" -> {
                if (value.toString().isBlank() && args.isNotEmpty()) {
                    args[0]
                } else value
            }
            else -> value
        }
    }

    private fun processConditionals(content: String, variables: Map<String, Any?>): String {
        val matcher = CONDITIONAL_PATTERN.matcher(content)
        val result = StringBuffer()
        
        while (matcher.find()) {
            val condition = matcher.group(1).trim()
            val conditionContent = matcher.group(2)
            
            val replacement = if (evaluateCondition(condition, variables)) {
                conditionContent
            } else {
                ""
            }
            
            matcher.appendReplacement(result, escape(replacement))
        }
        matcher.appendTail(result)
        
        return result.toString()
    }

    private fun processLoops(content: String, variables: Map<String, Any?>): String {
        val matcher = LOOP_PATTERN.matcher(content)
        val result = StringBuffer()
        
        while (matcher.find()) {
            val itemVar = matcher.group(1)
            val listVar = matcher.group(2)
            val loopContent = matcher.group(3)
            
            val list = getNestedValue(listVar, variables)
            val replacement = when (list) {
                is List<*> -> {
                    list.mapIndexed { index, item ->
                        val loopVars = variables.toMutableMap()
                        loopVars[itemVar] = item
                        loopVars["loop"] = mapOf(
                            "index" to index,
                            "index0" to index,
                            "index1" to index + 1,
                            "first" to (index == 0),
                            "last" to (index == list.size - 1),
                            "length" to list.size
                        )
                        processVariables(loopContent, loopVars)
                    }.joinToString("")
                }
                else -> ""
            }
            
            matcher.appendReplacement(result, escape(replacement))
        }
        matcher.appendTail(result)
        
        return result.toString()
    }

    private fun evaluateCondition(condition: String, variables: Map<String, Any?>): Boolean {
        // Simple condition evaluation - can be extended
        return when {
            condition.contains("==") -> {
                val parts = condition.split("==").map { it.trim() }
                if (parts.size == 2) {
                    val left = getNestedValue(parts[0], variables)?.toString() ?: ""
                    val right = parts[1].removeSurrounding("'").removeSurrounding("\\"")
                    left == right
                } else false
            }
            condition.contains("!=") -> {
                val parts = condition.split("!=").map { it.trim() }
                if (parts.size == 2) {
                    val left = getNestedValue(parts[0], variables)?.toString() ?: ""
                    val right = parts[1].removeSurrounding("'").removeSurrounding("\\"")
                    left != right
                } else false
            }
            else -> {
                // Variable existence check
                val value = getNestedValue(condition, variables)
                when (value) {
                    null -> false
                    is Boolean -> value
                    is String -> value.isNotBlank()
                    is List<*> -> value.isNotEmpty()
                    is Number -> value != 0
                    else -> true
                }
            }
        }
    }

    private fun generateFrontmatter(
        clipData: ClipData,
        metadata: Metadata?,
        highlights: List<Highlight>
    ): String {
        val now = Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault())
        
        return buildString {
            appendLine("---")
            appendLine("title: \\"${escape(clipData.title)}\\"")
            appendLine("url: ${clipData.url}")
            clipData.domain?.let { appendLine("domain: $it") }
            if (clipData.tags.isNotEmpty()) {
                appendLine("tags:")
                clipData.tags.forEach { tag ->
                    appendLine("  - $tag")
                }
            }
            appendLine("created: ${now.date}")
            appendLine("updated: ${now.date}")
            
            metadata?.let { meta ->
                meta.author?.let { appendLine("author: \\"${escape(it)}\\"") }
                meta.siteName?.let { appendLine("site_name: \\"${escape(it)}\\"") }
                meta.publishedAt?.let { appendLine("published: $it") }
                meta.wordCount?.let { appendLine("word_count: $it") }
                meta.description?.let { appendLine("description: \\"${escape(it)}\\"") }
            }
            
            if (highlights.isNotEmpty()) {
                appendLine("highlights:")
                highlights.forEach { highlight ->
                    appendLine("  - text: \\"${escape(highlight.text)}\\"")
                    highlight.note?.let { appendLine("    note: \\"${escape(it)}\\"") }
                }
            }
            
            appendLine("clipper: obsidian-android")
            appendLine("---")
        }
    }

    private fun generateFilename(
        template: Template,
        clipData: ClipData,
        variables: Map<String, Any?>
    ): String {
        val baseFilename = template.behavior.noteName 
            ?: clipData.title.ifBlank { "Untitled" }
        
        return sanitizeFilename(processVariables(baseFilename, variables))
    }

    private fun determineFolder(
        template: Template,
        clipData: ClipData,
        variables: Map<String, Any?>
    ): String {
        return template.behavior.folder
            ?: clipData.folder
            ?: "Clips"
    }

    private fun sanitizeFilename(filename: String): String {
        return filename
            .replace(Regex("[<>:\\"\\|\\?\\*]"), "")
            .replace("/", "-")
            .replace("\\\\", "-")
            .trim()
            .take(100)
            .ifBlank { "Untitled" }
    }

    private fun convertToMarkdown(html: String): String {
        // Basic HTML to Markdown conversion
        return html
            .replace(Regex("<strong>(.*?)</strong>"), "**$1**")
            .replace(Regex("<b>(.*?)</b>"), "**$1**")
            .replace(Regex("<em>(.*?)</em>"), "*$1*")
            .replace(Regex("<i>(.*?)</i>"), "*$1*")
            .replace(Regex("<a href=\\"(.*?)\\">(.*?)</a>"), "[$2]($1)")
            .replace(Regex("<br\\s*/?\\s*>"), "\\n")
            .replace(Regex("<p>(.*?)</p>"), "$1\\n\\n")
            .replace(Regex("<[^>]+>"), "") // Remove remaining HTML tags
            .trim()
    }

    private fun formatDate(value: Any?, format: String): String {
        // Simplified date formatting
        return try {
            val now = Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault())
            when (format) {
                "yyyy-MM-dd" -> now.date.toString()
                "HH:mm:ss" -> now.time.toString()
                else -> now.toString()
            }
        } catch (e: Exception) {
            value?.toString() ?: ""
        }
    }

    private fun escape(text: String): String {
        return text.replace("\\\\", "\\\\\\\\")
            .replace("$", "\\\\$")
    }
}

data class ProcessedTemplate(
    val content: String,
    val frontmatter: String,
    val filename: String,
    val folder: String
)
'''
}

print("Advanced Android components created!")
for filename in advanced_components.keys():
    print(f"- {filename}")

# Save the advanced components
for filename, content in advanced_components.items():
    with open(filename, 'w') as f:
        f.write(content)

print(f"\nCreated {len(advanced_components)} advanced component files")