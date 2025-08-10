
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
            val fullContent = processedTemplate.frontmatter + "\n" + processedTemplate.content

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
            .replace(Regex("[<>:\"\|\?\*]"), "")
            .replace("/", "-")
            .replace("\\", "-")
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
