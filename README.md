# LTL based runtime verification digital twin framework

Protecting users and assets from cyber-attacks is one of the most critical problems in cyberspace. Alteration of engineering data is a cyber-attack in cyber-physical systems and IoT systems which can cause system damage and harm to users. Modelling and simulations-based testing are often insufficient to defend against attacks. To address the cyber-security challenge, we present a runtime verification-based digital twin framework that combines the strengths of data analytics and Linear Temporal Logic (LTL) formula learning. This work investigates how to extract the LTL formula from historical data. Our procedure processes the past data into the required format and then performs clustering of the data points. Once the cluster of interest is identified, we then process the data further to form sequences that represent the trend of the pattern. The data sequences are passed into an LTL learning algorithm, and we obtain an LTL formula that represents the pattern to be detected. This procedure is integrated into our runtime framework to form a holistic approach. We demonstrate and evaluate our approach using several datasets in cyber-physical systems. 

The methodology is a runtime verification-based digital twin framework that combines the strengths of data analytic and Linear Temporal Logic (LTL) formula learning. Shown in [Figure](https://github.com/deejay2206/LTL-based-Runtime-Verification/blob/50d58144d8dca8200a94dc24af4c33637fae3b5b/Architecture.png) is a systematic approach and is divided into four phases as follows:
```
• Phase I: Historical Data Processing
• Phase II: Data Clustering
• Phase III: Domain Expert Analysis
• Phase IV: LTL Formula Learning
• Phase V: Runtime Checking
```
# Phase I: Historical Data Processing
To commence the process of learning LTL formula peculiar to any given system, historical data processing is the first phase as indicated in [Figure](https://github.com/deejay2206/LTL-based-Runtime-Verification/blob/50d58144d8dca8200a94dc24af4c33637fae3b5b/Architecture.png). The raw data set requires pre-processing and this involves data dimension reduction and data encoding such that the application or computer is able to read and interpret.

Some computer applications are unable to process categorical variables because they have no meaning to the applications. Therefore the data variables have to be processed which includes converting them to what the application can understand. This action is called data pre-processing.

# Phase II: Data Clustering
The next step in the LTL based runtime verification framework is data clustering. Given the type of engineering data obtained which is an unlabeled dataset, we deploy an unsupervised learning approach using the K-means algorithm. Using the K-means algorithm, we learn the dataset patterns or data groupings without the need for human intervention.

With K-means clustering, data points are classified into **K** groups, where `K' represents the number of clusters based on the distance from each group’s centroid. The data points closest to a given centroid will be clustered under the same category. A larger **K** value will indicate smaller groupings with more granularity whereas a smaller **K** value will have larger groupings and less granularity. As part of the steps in the K-means clustering, instead of a random selection of a number of clusters, we calculate an optimal number based on the scientific data using the elbow method. Using a python script, the processed data obtained from CubeSat was clustered using the K-means algorithm. With the domain expert analysis, the cluster(s) representing ***bad states*** and ***good state*** are identified. 

For the phase I and II, run the [data process](https://github.com/deejay2206/LTL-based-Runtime-Verification/blob/62a259a06c95fb984c83cbf771bbdf95e433e02c/data_formation_script) using python3 data_formation_script.py.

# Phase III: Domain Expert Analysis
The third phase of our approach is domain expert analysis. A domain expert assists in identifying which of the clusters present a normal behaviour of the system. 

With the domain expert analysis, we identify a cluster that represents a ***good state*** and a cluster representing a ***bad state***. Based on the outcome of the clustering algorithm and domain expert analysis, we classify the data into clusters, indicative of ***good state*** and ***bad state***, identify the ***bad state*** instance and locate it in the time series. We further extract ***n*** consecutive instances leading to the ***bad state*** instance in the time series, where ***n*** presents a numeric value. This extraction would serve as a positive trace while the***bad state*** instances serve as a negative trace. The output is stored as a trace file to be injected into the LTL formula learning algorithm to formulate the LTL formula that represents the system. From the extracted file stored as [example.trace] consisting of sequence of traces, partitioned into positive and negative traces using ***---*** as separator with positive as the first set.

Before learning the \ac{ltl} formula, the variables in the trace file are translated into 1s and 0s for the purpose of the \ac{ltl} formula learning application. Hence, the clustering technique or statistical measures such as standard deviation can be deployed on each feature or column to generate a trace file.

# Phase IV: LTL Formula Learning
The next phase of our approach is the LTL formula learning. At this phase, an LTL formula is generated based on the historical data set. In order to learn the LTL formulae, we implement the [Scarlet algorithm](https://github.com/rajarshi008/Scarlet). 

after generating a trace file from the data analysis which contains positive and negative traces. The normal traffic is tagged as a set of positive (***P***) traces, and the abnormal traffic is tagged as a set of negative (***N***) traces. The generated formula serves as a model for every trace in ***P*** and not a model for any of the traces from ***N***.

We learn the LTL formula from the trace file using Scarlet. Each trace is a sequence of states separated by ***;*** and each state represents the truth value of atomic propositions. An example of a trace is 1,0,1;0,0,0;0,1,1 which consists of three states each of which defines the values of three propositions and by default considered to be p,q,r. 

At this phase, we formulate the linear temporal logic (LTL) properties for our runtime verification of the digital twin-based satellite infrastructure. The formulae serves as property to be declared in our runtime monitor. Given the transition system (TS) and LTL formula ***φ***, we can check if ***φ*** holds in the TS or not. 
