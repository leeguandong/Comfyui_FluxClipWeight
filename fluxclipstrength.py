# We aren't just doing 1 or 10, We have 100,000 max strength! (for excessive experimentation)


class CLIPTextEncodeFluxWeight:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP",),
                "clip_l": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "t5xxl": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "clip_l_strength": ("FLOAT", {"default": 500.0, "min": 0.0, "max": 100000.0, "step": 0.01}),
                "t5xxl_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 100000.0, "step": 0.01}),
                "guidance": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 100000.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "advanced/conditioning/flux"

    def encode(self, clip, clip_l, t5xxl, clip_l_strength, t5xxl_strength, guidance):
        print("Tokenizing clip_l and t5xxl texts")
        tokens_l = clip.tokenize(clip_l)["l"]
        print(f"tokens_l: {tokens_l}")
        tokens_t5 = clip.tokenize(t5xxl)["t5xxl"]
        print(f"tokens_t5: {tokens_t5}")

        print("Combining tokens into token_weights dictionary")
        token_weights = {"l": tokens_l, "t5xxl": tokens_t5}
        print(f"token_weights: {token_weights}")

        print("Encoding tokens with clip.encode_from_tokens")
        output = clip.encode_from_tokens(token_weights, return_pooled=True, return_dict=True)
        print(f"output: {output}")

        # Apply strengths
        cond = output.pop("cond")
        print(f"cond before strength adjustment: {cond}")

        # Apply strengths to tensors directly
        if cond.dim() == 3:  # Check if the cond tensor has the correct dimensions
            cond[:, :, :1] *= clip_l_strength
            cond[:, :, 1:] *= t5xxl_strength

        print(f"cond after strength adjustment: {cond}")
        output["guidance"] = guidance
        return ([[cond, output]],)


NODE_CLASS_MAPPINGS = {
    "CLIPTextEncodeFluxWeight": CLIPTextEncodeFluxWeight,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPTextEncodeFluxWeight": "CLIPTextEncodeFluxWeight",
}
