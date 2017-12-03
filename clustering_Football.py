#----------------- Step 1:  Importing required packages for this problem ------------------------------------- 
   # data analysis and wrangling
    import pandas as pd
    import numpy as np
    import random as rn
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    
   # K-mean library
    from sklearn.cluster import KMeans
    import scipy.cluster.hierarchy as sch
    from sklearn.cluster import AgglomerativeClustering
   
   # visualization
    import seaborn as sns
    import matplotlib.pyplot as plt

#-----------------------------Step 2:Read CSV file--------------------------------------
      
    # loading train and test sets with pandas 
    FootballPlayerRecords = pd.read_csv('Song_Football.csv',encoding='latin-1')
   
    # Print the columns of dataframe
    print(FootballPlayerRecords.columns.values)
    
    # Returns first n rows
    FootballPlayerRecords.head(10)
    
    
    # Retrive data type of object and no. of non-null object
    FootballPlayerRecords.info()
    
    # Retrive details of integer and float data type 
    FootballPlayerRecords.describe()
    
    # To get  details of the categorical types
    FootballPlayerRecords.describe(include=['O'])

   

 #----------------------------Step 3: Preparing Data quality Report-----------------------

  # To get count of no. of NULL for each data type columns = full.columns.values
    columns = FootballPlayerRecords.columns.values
    data_types = pd.DataFrame(FootballPlayerRecords.dtypes, columns=['data types'])
    
    missing_data_counts = pd.DataFrame(FootballPlayerRecords.isnull().sum(),
                            columns=['Missing Values'])
    
    present_data_counts = pd.DataFrame(FootballPlayerRecords.count(), columns=['Present Values'])
    
    UniqueValues = pd.DataFrame(FootballPlayerRecords.nunique(), columns=['Unique Values'])
    
    MinimumValues = pd.DataFrame(columns=['Minimum Values'])
    for c in list(columns):
       if (FootballPlayerRecords[c].dtypes == 'float64' ) | (FootballPlayerRecords[c].dtypes == 'int64'):
            MinimumValues.loc[c]=FootballPlayerRecords[c].min()
       else:
            MinimumValues.loc[c]=0
 
    MaximumValues = pd.DataFrame(columns=['Maximum Values'])
    for c in list(columns):
       if (FootballPlayerRecords[c].dtypes == 'float64' ) |(FootballPlayerRecords[c].dtypes == 'int64'):
            MaximumValues.loc[c]=FootballPlayerRecords[c].max()
       else:
            MaximumValues.loc[c]=0
    
    data_quality_report=data_types.join(missing_data_counts).join(present_data_counts).join(UniqueValues).join(MinimumValues).join(MaximumValues)
    data_quality_report.to_csv('Data_report.csv', index=True) 
#----------------------------Step 4: Missing value treatment--------------------------------
   # There is no missing, no actions required

#----------------------------Step 5: outlier  treatment-------------------------------------
    # outliers doesn't affect clustering there is no need to remove or impute the oulier
    # If there are outlier they will automatically assign to a single cluster
  
#----------------------------Step 6: Check information about insured player Song -----------------
  
    song = FootballPlayerRecords.loc[FootballPlayerRecords['First_Name']=='Song',] 
    song


#----------------------------Step 7: Data preparation for clutering------------------------------

  # keeping only the numeric values
  # for clustering we don't need 1st column and use col 2:8
  FootballPlayerRecords_Clustering = FootballPlayerRecords.iloc[:,1:8]  
  
  #-----Scaling
  sc = StandardScaler()
  FootballPlayerRecords_Clustering = sc.fit_transform(FootballPlayerRecords_Clustering)
  # weighting tackles by 3
  FootballPlayerRecords_Clustering[:,0] = FootballPlayerRecords_Clustering[:,0] *3


#--------------Step 8: find the optimal number of clusters( K value) using elbow method----
    wcss=[]
   
    for i in range(1, 15):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        kmeans.fit(FootballPlayerRecords_Clustering)
        wcss.append(kmeans.inertia_)
        
    plt.plot(range(1, 15), wcss)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
   # According to Scatterplot , optimal k value =8

#-------------------Step 9: Building cluster and assigning to players records --------------
 
  Clusters_result = KMeans(n_clusters = 8, init = 'k-means++', random_state = 42) 
  Clusters_result.fit(FootballPlayerRecords_Clustering)
  
  FootballPlayerRecords['Cluster_no'] = Clusters_result.labels_
  
#------------------------Step 10: Finding players similar to Song -------------------------------
  
  Song_cluster = FootballPlayerRecords.loc[FootballPlayerRecords['First_Name']=='Song','Cluster_no']
  
  Players_similar_to_song =FootballPlayerRecords.loc[FootballPlayerRecords['Cluster_no']==0,]
                                                           
  
  Players_similar_to_song
  
  
  
#------------------------------Different Approch:Using Hierarchical cluster --------------
  
  # Using the dendrogram to find the optimal number of clusters
   dendrogram = sch.dendrogram(sch.linkage(FootballPlayerRecords_Clustering, method = 'ward'))
   plt.title('Dendrogram')
   plt.xlabel('Customers')
   plt.ylabel('Euclidean distances')
   plt.show()
      
   # Fitting Hierarchical Clustering to the dataset
  
   hc = AgglomerativeClustering(n_clusters = 8, affinity = 'euclidean', linkage = 'ward')
   hc.fit(FootballPlayerRecords_Clustering)
   
   FootballPlayerRecords['Cluster_no'] = hc.labels_
   
   Song_cluster = FootballPlayerRecords.loc[FootballPlayerRecords['First_Name']=='Song','Cluster_no']
  
   Players_similar_to_song =FootballPlayerRecords.loc[FootballPlayerRecords['Cluster_no']==1,]
                                                           
  
   Players_similar_to_song
    