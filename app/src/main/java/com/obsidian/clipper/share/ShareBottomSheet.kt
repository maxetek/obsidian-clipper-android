package com.obsidian.clipper.share

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
