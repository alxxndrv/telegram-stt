import transcription_service_pb2 as transcription_service_pb2
import transcription_service_pb2_grpc as transcription_service_pb2_grpc
import grpc
from concurrent import futures
import sys
import os
import convert
import transcribe
import download


class TranscriptionService(transcription_service_pb2_grpc.TranscriptionServiceServicer):
    def __init__(self):
        pass

    def TranscribeVoiceMessage(self, request, context):
        url = request.file_id
        file = download.download_file(url, 'files')
        transcription = transcribe.transcribe(file)

        return transcription_service_pb2.TranscriptionResponse(text=transcription)


def serve():
    if not os.path.isfile('gglm-medium.bin'):
        print('Downloading model..')
        download.download_file(
            'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin?download=true', './')
        print('Model downloaded.')

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transcription_service_pb2_grpc.add_TranscriptionServiceServicer_to_server(
        TranscriptionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
