from django.db import migrations

class Migration(migrations.Migration):

    # Make sure this points to YOUR actual last migration for chatapp
    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    # We need transaction=False because CREATE INDEX CONCURRENTLY cannot run in a transaction
    atomic = False

    operations = [
        # 1) Add the vector column (db-only; Django model field is optional)
        migrations.RunSQL(
            """
            ALTER TABLE chatapp_message
            ADD COLUMN IF NOT EXISTS embedding VECTOR(384);
            """,
            reverse_sql="""
            ALTER TABLE chatapp_message
            DROP COLUMN IF EXISTS embedding;
            """,
        ),

        # 2) (Optional but recommended) HNSW index for fast ANN search
        migrations.RunSQL(
            """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS chatapp_message_embedding_hnsw
            ON chatapp_message
            USING hnsw (embedding vector_cosine_ops);
            """,
            reverse_sql="""
            DROP INDEX CONCURRENTLY IF EXISTS chatapp_message_embedding_hnsw;
            """,
        ),
    ]
