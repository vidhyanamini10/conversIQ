# chatapp/management/commands/backfill_embeddings.py
from django.core.management.base import BaseCommand
from django.db import connection
from chatapp.models import Message
from chatapp.embeddings import embed_text

class Command(BaseCommand):
    help = "Generate embeddings for all messages that don't have one yet."

    def handle(self, *args, **options):
        messages = Message.objects.filter(embedding__isnull=True)
        total = messages.count()
        self.stdout.write(self.style.NOTICE(f"🧠 Backfilling {total} messages..."))

        for i, msg in enumerate(messages, start=1):
            vector = embed_text(msg.content)
            vector_literal = "[" + ",".join(str(x) for x in vector) + "]"

            with connection.cursor() as cur:
                cur.execute(
                    "UPDATE chatapp_message SET embedding = %s::vector WHERE id = %s",
                    [vector_literal, msg.id],
                )

            if i % 10 == 0 or i == total:
                self.stdout.write(self.style.SUCCESS(f"✅ {i}/{total} done"))

        self.stdout.write(self.style.SUCCESS("🎯 All embeddings backfilled successfully!"))
