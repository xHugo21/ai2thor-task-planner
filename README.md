# Task execution on the iTHOR simulator using automated planning and neural networks.
### :page_with_curl: Description

The main objective is to develop a program that allows the user to execute any action inside an iTHOR environment.

There are two ways of running the program:

1. Using metadata given by the simulator. Thanks to it we can know which objects are in a specific scene and their positions. Using this data we can then generate a PDDL problem to obtain an optimized plan. The plan is translated back to executable actions and triggered in order.

2. Using OGAMUS algorithm. OGAMUS is an algorithm developed by Leonardo Lamanna, Luciano Serafini, Alessandro Saetti, Alfonso Gerevini y Paolo Traverso which scans an iTHOR scene using pretrained neural network models and stores all the data it gets inside PDDL problem files. In this project the algorithm has been modified so it can run within an specific environment and so that actions can be chained. There is also the possibility to pass a PDDL problem as argument and translate the actions that want to be executed.

### :whale: Running with Docker

#### 1. Allow X11 connections
To enable GUI visualization from the container:
```bash
xhost +local:docker
```

#### 2. Build and Run

**CPU version:**
```bash
docker build -t ai2thor-task-planner:cpu -f Dockerfile .
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    ai2thor-task-planner:cpu
```

**GPU version (requires NVIDIA Docker):**
```bash
docker build -t ai2thor-task-planner:gpu -f Dockerfile.gpu .
docker run -it --rm --gpus all \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    ai2thor-task-planner:gpu
```

#### 3. Persisting Output Files

To save generated images, PDDL files, and results on your host machine, mount the corresponding volumes:
```bash
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $(pwd)/images:/app/images \
    -v $(pwd)/pddl/outputs:/app/pddl/outputs \
    -v $(pwd)/pddl/problems:/app/pddl/problems \
    -v $(pwd)/Results:/app/Results \
    ai2thor-task-planner:cpu
```

### :eyes: Results visualization

iTHOR simulator launches a visualization window every time an environment is generated. However, it is pretty hard to see if everything has executed correctly. The program extracts the following data on each action executed:

- scene.png: A zenithal shot of the scene so that the user can see the layout of the room. It is generated in /images/scene.png

![Zenithal shot of the scene FloorPlan1](/assets/example_scene.png)

- problemX_Y: An image of each step executed. X represents the action and Y the step.

![The agent positions in front of the objective: iter0_1](/assets/iter0_1.png) ![The agent picks up the objective: iter0_2](/assets/iter0_2.png)

- CLI data: When an action is finished, status about last action and objective is displayed.

- PDDL problem files in /pddl/problems/

- Plans generated in /pddl/outputs/

### :dizzy: Recommended settings

- Run the following command to prevent GNOME from launching the "Application not responds" window. This way the Unity window can be left more time without interruption before executing tasks

```bash
gsettings set org.gnome.mutter check-alive-timeout 60000
```

### :pencil2: References

- iTHOR documentation: https://ai2thor.allenai.org/ithor/documentation/
- LAMANNA, Leonardo, et al. Online grounding of symbolic planning domains in unknown environments. En Proceedings of the International Conference on Principles of Knowledge Representation and Reasoning. 2022. p. 511-521. [PDF](https://arxiv.org/pdf/2112.10007.pdf). [GitHub](https://github.com/LamannaLeonardo/OGAMUS)
- [Metric-FF](https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html) planner
- [tranchis](https://github.com/tranchis/metric-ff-macos) macos compilable version of [Metric-FF](https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html)
