# gemini_tts.py
import os
import mimetypes
import struct
from google import genai
from google.genai import types

# Initialize client (use your real API key)
client = genai.Client(api_key="AIzaSyDZ8paYyKfpxhgcsGQHprn2GM4Y3x350kE")

MODEL_NAME = "gemini-2.5-pro-preview-tts"


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Converts inline audio to WAV so Pi can play it with aplay."""
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE",
        b"fmt ", 16, 1, num_channels,
        sample_rate, byte_rate, block_align,
        bits_per_sample,
        b"data", data_size
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=")[1])
            except:
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L")[1])
            except:
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def gemini_tts(text: str, output_file="tts_output.wav"):
    """Generate speech with Gemini TTS and save as WAV."""
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=text)],
        ),
    ]

    config = types.GenerateContentConfig(
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Sulafat"
                )
            )
        ),
    )

    # Stream audio chunks
    for chunk in client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=config
    ):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
            and chunk.candidates[0].content.parts[0].inline_data
        ):
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            mime_type = inline_data.mime_type
            audio_bytes = inline_data.data

            # Convert to WAV
            if not mime_type.endswith("wav"):
                audio_bytes = convert_to_wav(audio_bytes, mime_type)

            # Save file
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            print(f"[Gemini TTS] Saved: {output_file}")
            return output_file

    print("[Gemini TTS] No audio received")
    return None