# Scheduler
#### Video Demo:  <URL HERE>
#### Description:
The program I made as my final project was inspired by my Operating Systems class at my university. We were learning about what scheduler algorithms operating systems use.

Since I had to be able to shedule tasks on paper, I thought writing a program to help check wherther I did a good job or not would be a good little project.

My program implements a complex **2 level** scheduler, where the lower priority algorithm is a **Shortest Remaining Time First** (SRTF) algorithm and the high priority one is **Round Robin** (RR).
#### Input:
The program uses stdin to gather the input form the user. Here is an example of how an input should look like:
```
A,0,0,6
B,0,1,5
C,1,5,2
D,1,10,1
```
- The task's name (A, B, C...)
- The task's priority (0 or 1)
- The task's starting time (integer >= 0)
- The task's length (integer >= 1)
#### Output:
```
ACABDB
A:2,B:8,C:0,D:0
```
- The first row displays the order in which the tasks ran
- The second row displays how long a task waited until it was completed
#### Future Plans:
- Rendering picture output with Pillow.
- Implementing multiple algorithms that can be swapped in and out.
- Adjustable level size for the scheduler.