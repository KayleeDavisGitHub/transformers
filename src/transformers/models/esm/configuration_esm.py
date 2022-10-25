# coding=utf-8
# Copyright 2021 Facebook and The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" ESM model configuration"""

from ...configuration_utils import PretrainedConfig
from ...utils import logging
from dataclasses import dataclass
from typing import Optional


logger = logging.get_logger(__name__)

# TODO Update this
ESM_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "facebook/esm1b": "https://huggingface.co/facebook/esm1b/resolve/main/config.json",
    # See all ESM models at https://huggingface.co/models?filter=esm
}


class EsmConfig(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a [`ESMModel`]. It is used to instantiate a ESM model
    according to the specified arguments, defining the model architecture. Instantiating a configuration with the
    defaults will yield a similar configuration to that of the ESM
    [esm-base-uncased](https://huggingface.co/esm-base-uncased) architecture.

    Configuration objects inherit from [`PretrainedConfig`] and can be used to control the model outputs. Read the
    documentation from [`PretrainedConfig`] for more information.


    Args:
        vocab_size (`int`, *optional*):
            Vocabulary size of the ESM model. Defines the number of different tokens that can be represented by the
            `inputs_ids` passed when calling [`ESMModel`].
        mask_token_id (`int`, *optional*):
            The index of the mask token in the vocabulary. This must be included in the config because of the
            "mask-dropout" scaling trick, which will scale the inputs depending on the number of masked tokens.
        pad_token_id (`int`, *optional*):
            The index of the padding token in the vocabulary. This must be included in the config because certain parts
            of the ESM code use this instead of the attention mask.
        hidden_size (`int`, *optional*, defaults to 768):
            Dimensionality of the encoder layers and the pooler layer.
        num_hidden_layers (`int`, *optional*, defaults to 12):
            Number of hidden layers in the Transformer encoder.
        num_attention_heads (`int`, *optional*, defaults to 12):
            Number of attention heads for each attention layer in the Transformer encoder.
        intermediate_size (`int`, *optional*, defaults to 3072):
            Dimensionality of the "intermediate" (often named feed-forward) layer in the Transformer encoder.
        hidden_act (`str` or `Callable`, *optional*, defaults to `"gelu"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`,
            `"relu"`, `"silu"` and `"gelu_new"` are supported.
        hidden_dropout_prob (`float`, *optional*, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        attention_probs_dropout_prob (`float`, *optional*, defaults to 0.1):
            The dropout ratio for the attention probabilities.
        max_position_embeddings (`int`, *optional*, defaults to 1026):
            The maximum sequence length that this model might ever be used with. Typically set this to something large
            just in case (e.g., 512 or 1024 or 2048).
        initializer_range (`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        layer_norm_eps (`float`, *optional*, defaults to 1e-12):
            The epsilon used by the layer normalization layers.
        position_embedding_type (`str`, *optional*, defaults to `"absolute"`):
            Type of position embedding. Choose one of `"absolute"`, `"relative_key"`, `"relative_key_query", "rotary"`.
            For positional embeddings use `"absolute"`. For more information on `"relative_key"`, please refer to
            [Self-Attention with Relative Position Representations (Shaw et al.)](https://arxiv.org/abs/1803.02155).
            For more information on `"relative_key_query"`, please refer to *Method 4* in [Improve Transformer Models
            with Better Relative Position Embeddings (Huang et al.)](https://arxiv.org/abs/2009.13658).
        use_cache (`bool`, *optional*, defaults to `True`):
            Whether or not the model should return the last key/values attentions (not used by all models). Only
            relevant if `config.is_decoder=True`.
        classifier_dropout (`float`, *optional*):
            The dropout ratio for the classification head.
        emb_layer_norm_before (`bool`, *optional*):
            Whether to apply layer normalization after embeddings but before the main stem of the network.
        token_dropout (`bool`, defaults to `False`):
            When this is enabled, masked tokens are treated as if they had been dropped out by input dropout.

    Examples:

    ```python
    >>> from transformers import EsmModel, EsmConfig

    >>> # Initializing a ESM esm-base-uncased style configuration >>> configuration = EsmConfig()

    >>> # Initializing a model from the configuration >>> model = ESMModel(configuration)

    >>> # Accessing the model configuration >>> configuration = model.config
    ```"""
    model_type = "esm"

    def __init__(
        self,
        vocab_size=None,
        mask_token_id=None,
        pad_token_id=None,
        hidden_size=768,
        num_hidden_layers=12,
        num_attention_heads=12,
        intermediate_size=3072,
        hidden_act="gelu",
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        max_position_embeddings=1026,
        initializer_range=0.02,
        layer_norm_eps=1e-12,
        position_embedding_type="absolute",
        use_cache=True,
        classifier_dropout=None,
        emb_layer_norm_before=None,
        token_dropout=False,
        is_folding_model=False,
        esmfold_config=None,
        structure_config=None,
        vocab_list=None,
        **kwargs
    ):
        super().__init__(pad_token_id=pad_token_id, **kwargs)

        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.hidden_act = hidden_act
        self.intermediate_size = intermediate_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.max_position_embeddings = max_position_embeddings
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps
        self.position_embedding_type = position_embedding_type
        self.use_cache = use_cache
        self.classifier_dropout = classifier_dropout
        self.emb_layer_norm_before = emb_layer_norm_before
        self.token_dropout = token_dropout
        self.mask_token_id = mask_token_id
        self.pad_token_id = pad_token_id
        self.is_folding_model = is_folding_model
        if is_folding_model:
            if esmfold_config is None:
                logger.info("No esmfold_config supplied for folding model, using default values.")
                esmfold_config = EsmFoldConfig()
            elif isinstance(esmfold_config, dict):
                esmfold_config = EsmFoldConfig(**esmfold_config)
            self.esmfold_config = esmfold_config

            if structure_config is None:
                logger.info("No structure_config supplied for folding model, using default values.")
                structure_config = StructureConfig()
            elif isinstance(structure_config, dict):
                structure_config = StructureConfig(**structure_config)
            self.structure_config = structure_config

            if vocab_list is None:
                logger.warning("No vocab_list supplied for folding model, assuming the ESM-2 vocabulary!")
                self.vocab_list = ('<cls>', '<pad>', '<eos>', '<unk>', 'L', 'A', 'G', 'V', 'S', 'E', 'R', 'T', 'I', 'D',
                                   'P', 'K', 'Q', 'N', 'F', 'Y', 'M', 'H', 'W', 'C', 'X', 'B', 'U', 'Z', 'O', '.', '-',
                                   '<null_1>', '<mask>')
            else:
                self.vocab_list = vocab_list
        else:
            self.esmfold_config = None
            self.structure_config = None
            self.vocab_list = None
        if self.esmfold_config is not None and self.esmfold_config.use_esm_attn_map:
            raise ValueError("The HuggingFace port of ESMFold does not support use_esm_attn_map at this time!")


@dataclass
class EsmFoldConfig:
    _name: str = "ESMFoldConfig"
    esm_type: str = None
    fp16_esm: bool = True
    use_esm_attn_map: bool = False
    esm_ablate_pairwise: bool = False
    esm_ablate_sequence: bool = False
    esm_input_dropout: float = 0

    embed_aa: bool = True
    bypass_lm: bool = False

    lddt_head_hid_dim: int = 128

    trunk_num_blocks: int = 48
    trunk_sequence_state_dim: int = 1024
    trunk_pairwise_state_dim: int = 128
    trunk_sequence_head_width: int = 32
    trunk_pairwise_head_width: int = 32
    trunk_position_bins: int = 32
    trunk_dropout: float = 0
    trunk_layer_drop: float = 0
    trunk_cpu_grad_checkpoint: bool = False
    trunk_max_recycles: int = 4
    trunk_chunk_size: Optional[int] = 128

@dataclass
class StructureConfig:
    # This is passed to OpenFold, so we can't really fold this into one of our config objects
    c_s: int = 384
    c_z: int = 128
    c_ipa: int = 16
    c_resnet: int = 128
    no_heads_ipa: int = 12
    no_qk_points: int = 4
    no_v_points: int = 8
    dropout_rate: float = 0.1
    no_blocks: int = 8
    no_transition_layers: int = 1
    no_resnet_blocks: int = 2
    no_angles: int = 7
    trans_scale_factor: int = 10
    epsilon: float = 1e-8
    inf: float = 1e5



