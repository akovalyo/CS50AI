# Project 4b: Nim

Write an AI that teaches itself to play Nim through reinforcement learning.

## Rules

**Nim** is a mathematical game of strategy in which two players take turns removing objects from distinct piles. On each turn, a player must remove at least one object, and may remove any number of objects provided they all come from the same pile. The goal of the game is to avoid taking the last object.

## Specification

AI learns the strategy for this game through reinforcement learning. By playing against itself repeatedly and learning from experience (here is 10 000 games), eventually AI will learn which actions to take and which actions to avoid.

In this project used **Q-learning**. Every result has a reward value (a number). An action that loses the game has a reward of -1, an action that results in the other player losing the game has a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.

Every time **AI** is in a state **s** and take an action **a**, it updates the Q-value Q(s, a) according to:

```
Q(s, a) <- Q(s, a) + alpha * (new value estimate - old value estimate)
```

where, **alpha** is the learning rate (how much we value new information compared to information we already have). The **new value estimate** represents the sum of the **reward received** for the current action and the estimate of all the **future rewards** that the player will receive. The **old value estimate** is just the existing value for Q(s, a). By applying this formula every time AI takes a new action, it learns which actions are better in any state.

## Optimal Strategy

Win in NIM game depends on two factors:

* The player who starts first.

* The initial configuration of the piles.

**Nim-sum** used to predict the winner of the game before playing the game.

**Nim-Sum** - is a cumulative XOR value of the numbers of objects in each pile at any point of the game.

**The winner in the game:**

*“If both A and B play optimally (they don’t make any mistakes), then the player starting first is guaranteed to win if the Nim-Sum at the beginning of the game is non-zero. Otherwise, if the Nim-Sum evaluates to zero, then player A will lose definitely.”*

**The optimal strategy** for each player is to make the Nim-Sum for his opponent zero in each of their turn, which will not be possible if it’s already zero.

In our case game starts with piles [1, 3, 5, 7]:

![pile](https://github.com/akovalyo/CS50AI/blob/master/week04/nim/src/nim-1.png?raw=true)

The **Nim-Sum** at the beginning of the game is **0**

So if your opponent won't make mistakes, you can not win the game if your move is first.

## Result:

* Correctly implemented AI should win most times when human starts first.

* If AI starts first, it should win if human will make mistake

*Video on youtube showing result*

[![Nim - youtube](https://img.youtube.com/vi/jvw-UBRwZ7g/0.jpg)](https://youtu.be/jvw-UBRwZ7g)