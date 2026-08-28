import torch
from time import perf_counter

class SelfAttentionV1:
    def slow_compute_attention_scores(self, inputs: torch.Tensor) -> torch.Tensor:
        attention_scores = torch.empty((inputs.shape[0], inputs.shape[0]))
        for i, x1 in enumerate(inputs): 
            for j, x2 in enumerate(inputs):
                attention_scores[i, j] = torch.dot(x1, x2)
        print(attention_scores)
        return attention_scores

    def fast_compute_attention_scores(self, inputs: torch.Tensor) -> torch.Tensor:
        attention_scores = inputs @ inputs.T
        print(attention_scores)
        return attention_scores

    def compute_attention_weights(self, attention_scores: torch.Tensor) -> torch.Tensor: 
        attention_weights = torch.softmax(attention_scores, dim=-1)
        print(attention_weights)
        return attention_weights
    
    def compute_context_vectors(self, attention_weights: torch.Tensor, inputs: torch.Tensor) -> torch.Tensor: 
        context_vectors = attention_weights @ inputs
        print(context_vectors)
        return context_vectors

def main(): 
    
    inputs = torch.tensor(
        [[0.43, 0.15, 0.89], # Your (x^1)
        [0.55, 0.87, 0.66], # journey (x^2)
        [0.57, 0.85, 0.64], # starts (x^3)
        [0.22, 0.58, 0.33], # with (x^4)
        [0.77, 0.25, 0.10], # one (x^5)
        [0.05, 0.80, 0.55]] # step (x^6)
    )
    sa = SelfAttentionV1()
    start = perf_counter()
    attention_scores = sa.fast_compute_attention_scores(inputs)
    attention_weights = sa.compute_attention_weights(attention_scores) 
    context_vectors = sa.compute_context_vectors(attention_weights, inputs)
    end = perf_counter()
    print(f"operation time: {end - start}")

if __name__ == "__main__": 
    main()