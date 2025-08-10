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
