from transcription_service_pb2_grpc import TranscriptionServiceStub
import grpc
import os

transcription_host = os.getenv("TRANSCRIPTION_HOST", "localhost")
transcription_channel = grpc.insecure_channel(
    f"{transcription_host}:50051"
)

transcription_client = TranscriptionServiceStub(transcription_channel)
