# Quick reference guide

## How to export a Quartznet .nemo file to a pure pytorch model?

```py
from thunder.quartznet.module import QuartznetModule
from thunder.data.dataset import AudioFileLoader
from thunder.quartznet.transform import patch_stft
import torch

module = QuartznetModule.load_from_nemo("/path/to/checkpoint.nemo")
# Uncomment the following line if exporting to onnx or mobile use
# module.audio_transform = patch_stft(module.audio_transform)
module.to_torchscript("model_ready_for_inference.pt")

# Optional step: also export audio loading pipeline
loader = AudioFileLoader(sample_rate=16000)
scripted_loader = torch.jit.script(loader)
scripted_loader.save("audio_loader.pt")
```

!!! note
    If the model uses features based on stft (quartznet, citrinet) and you're exporting to onnx
    or to use in mobile apps, there's one additional step before exporting that will replace the
    `torch.stft` operator to a custom implementation that works in those environments.
    Related issues:
    [pytorch](https://github.com/pytorch/pytorch/issues/31317),
    [torchaudio](https://github.com/pytorch/audio/issues/408),
    [onnx](https://github.com/onnx/onnx/issues/1646)


## How to run inference on that exported file?


``` python
import torch
import torchaudio

model = torch.jit.load("model_ready_for_inference.pt")
loader = torch.jit.load("audio_loader.pt")
# Open audio
audio = loader("audio_file.wav")
# transcriptions is a list of strings with the captions.
transcriptions = model.predict(audio)
```

## What if I want the probabilities instead of the captions?

Instead of `model.predict(audio)`, use just `model(audio)`

``` python hl_lines="8"
import torch
import torchaudio

model = torch.jit.load("model_ready_for_inference.pt")
loader = torch.jit.load("audio_loader.pt")
# Open audio
audio = loader("audio_file.wav")
probs = model(audio)
# If you also want the transcriptions:
transcriptions = model.text_transform.decode_prediction(probs.argmax(1))
```


## How to finetune a model if I already have the nemo manifests prepared?

``` python
import pytorch_lightning as pl

from thunder.data.datamodule import ManifestDatamodule
from thunder.quartznet.module import QuartznetModule,  QuartznetCheckpoint
from thunder.callbacks import FinetuneEncoderDecoder

dm = ManifestDatamodule(
    train_manifest="/path/to/train_manifest.json",
    val_manifest="/path/to/val_manifest.json",
    test_manifest="/path/to/test_manifest.json",
)
# Tab completion works to discover other QuartznetCheckpoint.*
model = QuartznetModule.load_from_nemo(QuartznetCheckpoint.QuartzNet5x5LS_En)

trainer = pl.Trainer(
    gpus=-1, # Use all gpus
    max_epochs=10,
    callbacks=[FinetuneEncoderDecoder(unfreeze_encoder_at_epoch=1)],
)

trainer.fit(model=model, datamodule=dm)
```

## How to get the initial_vocab_tokens from my dataset?

```python
from thunder.text_processing.tokenizer import char_tokenizer, get_most_frequent_tokens

my_datamodule = CustomDatamodule(...)
my_datamodule.prepare_data()
my_datamodule.setup(None)

train_corpus = " ".join(my_datamodule.train_dataset.all_outputs())
initial_vocab_tokens = get_most_frequent_tokens(train_corpus, char_tokenizer)
```
