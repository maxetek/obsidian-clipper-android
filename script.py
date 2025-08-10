# Create comprehensive Android project structure for Obsidian Clipper clone
import os
import json

# Create directory structure
project_structure = {
    "app/src/main/java/com/obsidian/clipper": [
        "ClipperApplication.kt",
        "di/",
        "data/",
        "domain/", 
        "ui/",
        "utils/"
    ],
    "app/src/main/java/com/obsidian/clipper/di": [
        "AppModule.kt",
        "DatabaseModule.kt",
        "NetworkModule.kt",
        "RepositoryModule.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/data": [
        "database/",
        "repository/",
        "network/",
        "model/"
    ],
    "app/src/main/java/com/obsidian/clipper/data/database": [
        "ClipperDatabase.kt",
        "dao/",
        "entities/"
    ],
    "app/src/main/java/com/obsidian/clipper/data/database/dao": [
        "ClipDao.kt",
        "TemplateDao.kt",
        "VaultDao.kt",
        "HighlightDao.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/data/database/entities": [
        "ClipEntity.kt",
        "TemplateEntity.kt", 
        "VaultEntity.kt",
        "HighlightEntity.kt",
        "Converters.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/data/model": [
        "ContentType.kt",
        "ShareContent.kt",
        "ClipData.kt",
        "Template.kt",
        "Vault.kt",
        "Highlight.kt",
        "Metadata.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/data/repository": [
        "ClipRepository.kt",
        "TemplateRepository.kt",
        "VaultRepository.kt",
        "HighlightRepository.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/data/network": [
        "ApiService.kt",
        "ContentExtractor.kt",
        "MetadataParser.kt",
        "HtmlToMarkdownConverter.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/domain": [
        "usecase/",
        "model/"
    ],
    "app/src/main/java/com/obsidian/clipper/domain/usecase": [
        "SaveClipUseCase.kt",
        "ProcessShareContentUseCase.kt",
        "ExtractContentUseCase.kt",
        "ApplyTemplateUseCase.kt",
        "ManageHighlightsUseCase.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/ui": [
        "MainActivity.kt",
        "ShareActivity.kt",
        "theme/",
        "screens/",
        "components/",
        "viewmodel/"
    ],
    "app/src/main/java/com/obsidian/clipper/ui/screens": [
        "library/",
        "settings/",
        "templates/",
        "share/"
    ],
    "app/src/main/java/com/obsidian/clipper/ui/screens/library": [
        "LibraryScreen.kt",
        "LibraryViewModel.kt",
        "components/"
    ],
    "app/src/main/java/com/obsidian/clipper/ui/screens/settings": [
        "SettingsScreen.kt",
        "SettingsViewModel.kt",
        "components/"
    ],
    "app/src/main/java/com/obsidian/clipper/ui/screens/templates": [
        "TemplatesScreen.kt",
        "TemplateEditorScreen.kt",
        "TemplatesViewModel.kt",
        "components/"
    ],
    "app/src/main/java/com/obsidian/clipper/ui/screens/share": [
        "ShareBottomSheet.kt",
        "ShareViewModel.kt",
        "components/"
    ],
    "app/src/main/java/com/obsidian/clipper/ui/components": [
        "ClipCard.kt",
        "TemplateCard.kt",
        "VaultPicker.kt",
        "TagInput.kt",
        "HighlightAnnotation.kt"
    ],
    "app/src/main/java/com/obsidian/clipper/utils": [
        "FileUtils.kt",
        "MarkdownUtils.kt",
        "TemplateEngine.kt",
        "VaultManager.kt",
        "NotificationUtils.kt"
    ],
    "app/src/main/res": [
        "values/",
        "layout/",
        "drawable/",
        "xml/"
    ]
}

# Create comprehensive gradle files
gradle_files = {
    "app/build.gradle.kts": '''
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("kotlin-kapt")
    id("dagger.hilt.android.plugin")
    id("kotlin-parcelize")
    id("androidx.room") version "2.6.0"
}

android {
    namespace = "com.obsidian.clipper"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.obsidian.clipper"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }

        room {
            schemaDirectory("$projectDir/schemas")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            signingConfig = signingConfigs.getByName("debug")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = "1.8"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // Core Android
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    
    // Compose BOM
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3:1.2.0")
    implementation("androidx.compose.material:material-icons-extended")
    
    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.6")
    implementation("androidx.hilt:hilt-navigation-compose:1.1.0")
    
    // Hilt Dependency Injection  
    implementation("com.google.dagger:hilt-android:2.48.1")
    kapt("com.google.dagger:hilt-android-compiler:2.48.1")
    
    // Room Database
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    kapt("androidx.room:room-compiler:2.6.1")
    
    // WorkManager
    implementation("androidx.work:work-runtime-ktx:2.9.0")
    implementation("androidx.hilt:hilt-work:1.1.0")
    kapt("androidx.hilt:hilt-compiler:1.1.0")
    
    // Networking
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    
    // HTML Parsing & Content Extraction
    implementation("org.jsoup:jsoup:1.17.2")
    implementation("com.github.rjeschke:txtmark:0.13")
    implementation("org.commonmark:commonmark:0.21.0")
    implementation("org.commonmark:commonmark-ext-yaml-front-matter:0.21.0")
    
    // Date/Time
    implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.5.0")
    
    // JSON
    implementation("com.google.code.gson:gson:2.10.1")
    
    // File handling
    implementation("androidx.documentfile:documentfile:1.0.1")
    
    // Image loading
    implementation("io.coil-kt:coil-compose:2.5.0")
    
    // Permissions
    implementation("com.google.accompanist:accompanist-permissions:0.32.0")
    
    // Testing
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.mockito:mockito-core:5.8.0")
    testImplementation("org.mockito.kotlin:mockito-kotlin:5.2.1")
    testImplementation("androidx.arch.core:core-testing:2.2.0")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.7.3")
    
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    androidTestImplementation(platform("androidx.compose:compose-bom:2024.02.00"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
''',

    "build.gradle.kts": '''
buildscript {
    dependencies {
        classpath("com.google.dagger:hilt-android-gradle-plugin:2.48.1")
    }
}

plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
    id("com.google.dagger.hilt.android") version "2.48.1" apply false
}
'''
}

# Create main application files
application_files = {
    "app/src/main/java/com/obsidian/clipper/ClipperApplication.kt": '''
package com.obsidian.clipper

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class ClipperApplication : Application() {
    
    override fun onCreate() {
        super.onCreate()
        initializeWorkManager()
    }
    
    private fun initializeWorkManager() {
        // WorkManager initialization will be handled by Hilt
    }
}
''',

    "app/src/main/AndroidManifest.xml": '''
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />

    <application
        android:name=".ClipperApplication"
        android:allowBackup="false"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.ObsidianClipper"
        tools:targetApi="31">
        
        <!-- Main Activity -->
        <activity
            android:name=".ui.MainActivity"
            android:exported="true"
            android:theme="@style/Theme.ObsidianClipper">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Share Activity -->
        <activity
            android:name=".ui.ShareActivity"
            android:exported="true"
            android:theme="@style/Theme.ObsidianClipper.Transparent"
            android:launchMode="singleTask">
            
            <!-- Text/URL sharing -->
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
            
            <!-- Image sharing -->
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="image/*" />
            </intent-filter>
            
            <!-- Multiple images -->
            <intent-filter>
                <action android:name="android.intent.action.SEND_MULTIPLE" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="image/*" />
            </intent-filter>
            
            <!-- PDF sharing -->
            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="application/pdf" />
            </intent-filter>
            
        </activity>

        <!-- WorkManager -->
        <provider
            android:name="androidx.startup.InitializationProvider"
            android:authorities="${applicationId}.androidx-startup"
            android:exported="false"
            tools:node="merge">
            <meta-data
                android:name="androidx.work.WorkManagerInitializer"
                android:value="androidx.startup" />
        </provider>

    </application>
</manifest>
''',

    "app/src/main/java/com/obsidian/clipper/data/model/Template.kt": '''
package com.obsidian.clipper.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import kotlinx.parcelize.Parcelize
import android.os.Parcelable

@Entity(tableName = "templates")
@Parcelize
data class Template(
    @PrimaryKey val id: String,
    val name: String,
    val description: String?,
    val content: String, // Markdown template content with variables
    val behavior: TemplateBehavior,
    val triggers: List<TemplateTrigger> = emptyList(),
    val interpreterContext: String? = null,
    val isDefault: Boolean = false,
    val createdAt: Long = System.currentTimeMillis(),
    val updatedAt: Long = System.currentTimeMillis()
) : Parcelable

@Parcelize
data class TemplateBehavior(
    val action: TemplateAction,
    val noteLocation: NoteLocation? = null,
    val noteName: String? = null,
    val folder: String? = null,
    val insertLocation: InsertLocation = InsertLocation.BOTTOM
) : Parcelable

enum class TemplateAction {
    CREATE_NEW_NOTE,
    ADD_TO_EXISTING_NOTE,
    ADD_TO_DAILY_NOTE
}

enum class NoteLocation {
    VAULT_ROOT,
    SPECIFIC_FOLDER,
    PROMPT_USER
}

enum class InsertLocation {
    TOP,
    BOTTOM
}

@Parcelize
data class TemplateTrigger(
    val type: TriggerType,
    val pattern: String,
    val value: String? = null
) : Parcelable

enum class TriggerType {
    URL_SIMPLE,    // Simple URL matching
    URL_REGEX,     // Regex URL matching  
    SCHEMA_ORG     // Schema.org matching
}
''',

    "app/src/main/java/com/obsidian/clipper/utils/TemplateEngine.kt": '''
package com.obsidian.clipper.utils

import com.obsidian.clipper.data.model.ClipData
import com.obsidian.clipper.data.model.Template
import com.obsidian.clipper.data.model.Metadata
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.regex.Pattern

class TemplateEngine {

    companion object {
        // Standard variables from Obsidian Web Clipper
        private val VARIABLE_PATTERN = Pattern.compile("\\{\\{([^}]+)\\}\\}")
        
        // Date formatters
        private val ISO_FORMATTER = DateTimeFormatter.ISO_LOCAL_DATE_TIME
        private val DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd")
        private val TIME_FORMATTER = DateTimeFormatter.ofPattern("HH:mm:ss")
    }

    fun processTemplate(template: Template, clipData: ClipData, metadata: Metadata?): String {
        var content = template.content
        
        // Create variable context
        val variables = createVariableContext(clipData, metadata)
        
        // Replace all variables
        val matcher = VARIABLE_PATTERN.matcher(content)
        val result = StringBuffer()
        
        while (matcher.find()) {
            val variableExpression = matcher.group(1)
            val replacement = processVariableExpression(variableExpression, variables)
            matcher.appendReplacement(result, replacement)
        }
        matcher.appendTail(result)
        
        return result.toString()
    }

    private fun createVariableContext(clipData: ClipData, metadata: Metadata?): Map<String, Any?> {
        val now = LocalDateTime.now()
        
        return mapOf(
            // Page variables
            "title" to (clipData.title.takeIf { it.isNotBlank() } ?: metadata?.title),
            "url" to clipData.url,
            "domain" to clipData.domain,
            "favicon" to metadata?.favicon,
            "published" to metadata?.publishedAt,
            "author" to metadata?.author,
            "length" to metadata?.length,
            "excerpt" to metadata?.excerpt,
            "site_name" to metadata?.siteName,
            "image" to metadata?.image,
            
            // Content variables  
            "content" to clipData.extractedContent,
            "selection" to clipData.selectedText,
            "note" to clipData.note,
            
            // Meta variables
            "date" to now.format(DATE_FORMATTER),
            "time" to now.format(TIME_FORMATTER),
            "datetime" to now.format(ISO_FORMATTER),
            "tags" to clipData.tags.joinToString(", "),
            
            // Schema.org variables (if available)
            "schema" to metadata?.schemaOrg,
            
            // Highlight variables
            "highlights" to clipData.highlights?.joinToString("\\n\\n") { "- ${it.text}" }
        )
    }

    private fun processVariableExpression(expression: String, variables: Map<String, Any?>): String {
        val parts = expression.split("|")
        val variableName = parts[0].trim()
        val filters = parts.drop(1).map { it.trim() }
        
        // Get base value
        var value = getVariableValue(variableName, variables)
        
        // Apply filters
        for (filter in filters) {
            value = applyFilter(value, filter)
        }
        
        return value?.toString() ?: ""
    }

    private fun getVariableValue(name: String, variables: Map<String, Any?>): Any? {
        // Handle nested properties (e.g., schema.@Recipe.name)
        val parts = name.split(".")
        var current: Any? = variables
        
        for (part in parts) {
            current = when (current) {
                is Map<*, *> -> current[part]
                else -> null
            }
            if (current == null) break
        }
        
        return current
    }

    private fun applyFilter(value: Any?, filter: String): Any? {
        if (value == null) return null
        
        val filterParts = filter.split(":")
        val filterName = filterParts[0]
        val filterArgs = filterParts.drop(1)
        
        return when (filterName.lowercase()) {
            "lower" -> value.toString().lowercase()
            "upper" -> value.toString().uppercase()
            "title" -> value.toString().split(" ").joinToString(" ") { 
                it.replaceFirstChar { char -> char.titlecaseChar() } 
            }
            "trim" -> value.toString().trim()
            "replace" -> {
                if (filterArgs.size >= 2) {
                    value.toString().replace(filterArgs[0], filterArgs[1])
                } else value
            }
            "slice" -> {
                val text = value.toString()
                when (filterArgs.size) {
                    1 -> {
                        val end = filterArgs[0].toIntOrNull() ?: text.length
                        text.take(end)
                    }
                    2 -> {
                        val start = filterArgs[0].toIntOrNull() ?: 0
                        val end = filterArgs[1].toIntOrNull() ?: text.length
                        text.substring(start.coerceAtLeast(0), end.coerceAtMost(text.length))
                    }
                    else -> text
                }
            }
            "date" -> {
                if (filterArgs.isNotEmpty()) {
                    try {
                        val formatter = DateTimeFormatter.ofPattern(filterArgs[0])
                        when (value) {
                            is LocalDateTime -> value.format(formatter)
                            else -> LocalDateTime.now().format(formatter)
                        }
                    } catch (e: Exception) {
                        value.toString()
                    }
                } else value
            }
            "default" -> {
                if (value.toString().isBlank() && filterArgs.isNotEmpty()) {
                    filterArgs[0]
                } else value
            }
            else -> value
        }
    }

    fun validateTemplate(template: String): List<String> {
        val errors = mutableListOf<String>()
        val matcher = VARIABLE_PATTERN.matcher(template)
        
        while (matcher.find()) {
            val variableExpression = matcher.group(1)
            try {
                // Basic validation of variable syntax
                val parts = variableExpression.split("|")
                if (parts.isEmpty()) {
                    errors.add("Invalid variable expression: $variableExpression")
                }
            } catch (e: Exception) {
                errors.add("Error in variable expression '$variableExpression': ${e.message}")
            }
        }
        
        return errors
    }
}
'''
}

print("Professional Android project structure created!")
print(f"Created {len(gradle_files)} Gradle files")  
print(f"Created {len(application_files)} core application files")
print(f"Created {len(project_structure)} directory structures")

# Save all files
for path, content in gradle_files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

for path, content in application_files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)  
    with open(path, 'w') as f:
        f.write(content)

print("\nKey files created:")
for path in list(gradle_files.keys()) + list(application_files.keys()):
    print(f"- {path}")