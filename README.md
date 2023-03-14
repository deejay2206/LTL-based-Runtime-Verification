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
