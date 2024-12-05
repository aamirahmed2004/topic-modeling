# Latent Dirichlet Allocation Explanation

In this document, I will attempt to explain my understanding of Latent Dirichlet Allocation; what it tries to achieve, the math and statistics behind the model, and how its parameters can be estimated with Gibbs Sampling. This is based on the 2003 paper by Blei et al., and the explanations are heavily inspired by https://www.youtube.com/@SerranoAcademy's LDA playlist, which really helped me grasp the concepts behind LDA.

Some preliminary definitions:

- Multinomial distribution, sometimes denoted **Multinomial($\theta$)**: it is a discrete probability distribution that is an extension of the Binomial distribution (which models the results of events with 2 outcomes, like a coin toss) to the case where there are multiple outcomes. $\theta$ is a parameter that describes the probabilities associated with each outcome. For example, rolling dice has 6 equally likely outcomes, so here: $$\theta = (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)$$ Another example is picking 1 marble out of a bag with 3 red marbles, 5 blue marbles, and 2 green marbles. Noting that there are 10 total marbles, here: $$\theta = (3/10, 5/10, 2/10)$$ It is important to note that all the entries of $\theta$ must sum to 1 (as they are probabilities).

- Beta distribution, denoted **Beta($\alpha, \beta$)**: it is a continuous probability distribution, which models the probability of picking a value between **0 and 1**, depending on the parameters $\alpha$ and $\beta$ (note that they must be positive real numbers). The probability density functions for a few combinations of $\alpha$ and $\beta$ are below:

  ![Beta Distribution Examples](/images/beta_pdf.svg)

  For  $\alpha = 2, \beta = 2$: 0.5 is the most likely outcome.

- Dirichlet distribution, denoted Dir($\alpha$): is a generalization of the Beta distribution to $k$ dimensions. The parameter $\alpha$ is not the same as the one from the Beta distribution. Here, $\alpha$ is a $k$-dimensional scalar vector (i.e. a list of $k$ numbers). For this explanation, consider the case that $\alpha$ is 3-dimensional, the values aren't important for now.

   Sampling such a Dirichlet distribution outputs a 3-dimensional vector, where
    1) each value is in the range [0,1] (just like the Beta distribution) and,
    2) all the 3 values sum to 1.

   For example: an output could be (0.3, 0.5, 0.2). Since these values *must* sum to 1, this vector can be considered a discrete probability distribution! Therefore, it can be said that the output of a Dirichlet distribution is itself a discrete probability distribution.

   But how do the values in $\alpha$ affect the probability of picking one of these vectors?

   ![symmetric Dir Distribution Examples](/images/dirichlet.gif)

   by Panos Ipeirotis, later modified by Love Sun and Dreams - [1], CC BY 3.0, https://commons.wikimedia.org/w/index.php?curid=10073606