
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
