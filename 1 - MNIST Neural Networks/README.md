# 1 - MNIST Neural Networks
## Intro
Hi, here is work I did at the start of 2025, picking apart a simple neural network example to develop my understanding of how these models work. The dataset used is MNIST hand drawn digits, in the zip file attached and also found here: https://git-disl.github.io/GTDLBench/datasets/mnist_datasets/

I am most proud of the pdf attached, which contains my own derivations of the gradients needed to perform gradient descent while training my neural networks. Doing this by hand has massively helped demystify neural network architecture for me.

It was a challenge to then implement these gradient calculations in Python, translating mathematical notation into NumPy code (and learning lots about how to write more efficient NumPy on the way... I have finally been forced to move away from list comprehension!)

My code is not the most efficient, but I am proud to have reached a point where **Nnet_class_improved.ipynb** can be used to train a neural network to 97+% accuracy on the unseen test dataset of 10,000 hand-drawn digits, all within ~2 hours.

*Note: The code and logic here is all written by me, though I must thank Chat GPT for being a great tutor during the course of this project, helping me explore gaps in my understanding of the theory behind neural networks and their modern implementations.*

## Table of Contents
Here are the files and a brief summary of each, enjoy:
### MNIST_CSV.zip
Zip file containing CSVs of the train and test MNIST datasets (28x28 pixel images of hand drawn digits)

### mnist_gradient_derivations_final.pdf
Follow me on my Vietnam travels as I derive the gradients of the cross-entropy loss function with respect to the bias and weight parameters in each layer of the network. I have never used the chain rule so many times, felt like unpacking russian dolls!

### rough_mnist_nnet.ipynb
My rough code, where all the ideas that made it into the final two python notebooks began. Lots of comments, and lots of experimentation. I learnt so much during this project, and it shows in this file.

### Nnet_class.ipynb
My first attempt at defining a class that can be used to train your own neural network on the MNIST dataset. In this first attempt, I had not learned about ways to improve efficiency/performance of training e.g. using mini-batches. So, the final output I arrived at was a network that took around a day of runtime to train (since I was using the entire dataset for each gradient step! And my code to calculate these gradients is SLOW lol). This network performed decently on unseen data, even correctly reading most digits on the cases Darya and I drew ourselves. However, improvements were made in the next file...

### Nnet_class_improved.ipynb
My final attempt (for now) at defining a class that can be used to train your own neural network on the MNIST dataset. Can be used to train a neural network to 97+% accuracy on the unseen test dataset of 10,000 hand-drawn digits, all within ~2 hours. 
