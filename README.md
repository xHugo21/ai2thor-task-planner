# Task execution on the iTHOR simulator using automated planning and neural networks.
### :page_with_curl: Description

The main objective is to develop a program that allows the user to execute any action inside an iTHOR environment.

There are two ways of running the program:

1. Using metadata given by the simulator. Thanks to it we can know which objects are in a specific scene and their positions. Using this data we can then generate a PDDL problem to obtain an optimized plan. The plan is translated back to executable actions and triggered in order.

2. Using OGAMUS algorithm. OGAMUS is an algorithm developed by Leonardo Lamanna, Luciano Serafini, Alessandro Saetti, Alfonso Gerevini y Paolo Traverso which scans an iTHOR scene using pretrained neural network models and stores all the data it gets inside PDDL problem files. In this project the algorithm has been modified so it can run within an specific environment and so that actions can be chained. There is also the possibility to pass a PDDL problem as argument and translate the actions that want to be executed.

### :computer: iTHOR simulator requirements

1. Operative System: macOS 10.9 o Ubuntu 14.04+ (recommended: Ubuntu 22.04)
2. Python: 3.5+
3. CPU with SSE2 instruction support
4. GPU: DX9 (shader model 3.0) or DX11 with feature level 9.3 capabilities
5. Linux users need X server with GLX module enabled

### :white_check_mark: Step by step installation

1. Meet simulator requirements

2. Clone repository into local folder
   ```
   git clone https://github.com/xHugo21/ai2thor-hugo.git
   ```
   ```
   cd ai2thor-hugo
   ```
3. Install Anaconda / Miniconda (recommended) and run the following command to install dependencies
   ```
   conda env create -n ai2thor -f environment.yml
   ```
4. Activate the conda environment

   ```
   conda activate ai2thor
   ```

5. Init and update the planner submodule

   ```
   git submodule init
   ```

   ```
   git submodule update
   ```

6. Compile the planner

   ```
   cd planner/metric-ff-macos/
   ```

   ```
   make
   ```

7. Download the pretrained neural network from the following link and drop the files into /Utils/pretrained_models/ [Pretrained Neural Network](https://drive.google.com/drive/folders/1UjADpBeBOMUKXQt-qSULIP3vM90zr_MR?usp=sharing)

8. Execute main.py and follow steps in CLI
   ```
   python main.py
   ```
9. If the user wants, he can pass a PDDL problem file as argument so that there is no need to select actions and objectives via CLI. This is only allowed for the OGAMUS method. There is a PDDL input example file at /pddl/inputs/example.pddl
   ```
   python main.py ./pddl/inputs/example.pddl
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

### :dizzy: Recommended improvements

- Run the following command to prevent GNOME from launching the "Application not responds" window. This way the Unity window can be left more time without interruption before executing tasks

```bash
gsettings set org.gnome.mutter check-alive-timeout 60000
```

### :pencil2: References

- iTHOR documentation: https://ai2thor.allenai.org/ithor/documentation/
- LAMANNA, Leonardo, et al. Online grounding of symbolic planning domains in unknown environments. En Proceedings of the International Conference on Principles of Knowledge Representation and Reasoning. 2022. p. 511-521. [PDF](https://arxiv.org/pdf/2112.10007.pdf). [GitHub](https://github.com/LamannaLeonardo/OGAMUS)
- [Metric-FF](https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html) planner
- [tranchis](https://github.com/tranchis/metric-ff-macos) macos compilable version of [Metric-FF](https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html)
