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

FOr the phase I and II, run the [script](https://github.com/deejay2206/LTL-based-Runtime-Verification/blob/526f3bd817734022210d32b62e4c0d191969a47a/Data%20Processing%20and%20Clustering%20script) using python .
