# Model-based SLAM

MobSLAM is a Simultaneous Localization and Mapping system for deformable environments.
Please refer to the [docs](docs) or the [homepage](https://pages.github.tik.uni-stuttgart.de/JHaag/Model_based_SLAM/) for more information on contents.


# Model-based SLAM

MobSLAM is a Simultaneous Localization and Mapping system for deformable environments.
This repository contains a graphical user interface that enables 

* the display of a [SOFA simulation](https://www.sofa-framework.org)
* different options to record and select different paths as well as a keyboard controller for the simulation camera
* different options to deform the simulated object
* use of a Simultaneous Localization and Mapping (SLAM) algorithm to 
	1. track the camera movement within the simulation 
	1. generate a map of the scene
	1. incorporate deformation information based on a parallel simulation

!(docs/images/main_gui2.png)

It is designed to be modular and easily extensible and aims at providing a reliable and replicable code base for future work on this topic.
