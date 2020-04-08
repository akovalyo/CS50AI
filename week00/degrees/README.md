# Project 0a: Degrees

## Description

Write a program that determines how many “degrees of separation” apart two actors are.  Based on [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon) game.

Anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that two actors both starred in.

In this problem, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

***

This is optimized version of the program. Instead of checking for a goal when the
node taken from frontier, it is checking nodes as they are added to the frontier. This improves efficiency significantly.


## Comparison

### TEST 1

**Version 1:**

![version1](https://raw.githubusercontent.com/akovalyo/CS50AI/master/week00/degrees/scr/scr_1.png)

**109 sec*

**Version 2:**

![version1](https://raw.githubusercontent.com/akovalyo/CS50AI/master/week00/degrees/scr/scr_1o.png)

**2 sec*

***

### TEST 2

**Version 1:**

![version2](https://raw.githubusercontent.com/akovalyo/CS50AI/master/week00/degrees/scr/scr_2.png)

**705 sec*

**Version 2:**

![version2](https://raw.githubusercontent.com/akovalyo/CS50AI/master/week00/degrees/scr/scr_2o.png)

**2.5 sec*


***

**Video that shows the functionality of the script**

[![Alt text](https://img.youtube.com/vi/QAjBharpQgU/0.jpg)](https://www.youtube.com/watch?v=QAjBharpQgU)