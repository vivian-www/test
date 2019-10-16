# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 17:56:45 2019

@author: Administrator
"""
#data_ori = data_ori.drop('时间',axis =1)
def miss_location(data_ori):
    '''
    计算数据的不连续点
    返回list
    '''
    
    datetime_diff = np.diff(data_ori['second']) # 计算时间的差分
    miss = []  # 返回的是异常值的位置
    for i in range(len(datetime_diff)):
        
        if datetime_diff[i] != -59 and datetime_diff[i] != 1:
            miss.append(i+1) # 返回的是异常值的位置
        
        else:
            pass
    
    return miss

miss = miss_location(data_ori)

def data_plus(data,location,sign):
    '''
    location 指的是缺失值返回的位置(单个缺失的位置，不是整个miss的结果)
    data表示原始数据
    找到第一个缺失位置，计算进行填补
    接着重新计算缺失位置，再进行填补
    sign为'no','yes'表示是否在一分钟内有缺失
    
    '''
#    
#    miss_len = data['second'][location+1]-data['second'][location]-1 # 需要填充的数据个数
#    data_new = pd.DataFrame()
#    data_new.columns = data.columns #
    
    miss_loca = location #输入的缺失数据的位置
    
    # 划分数据
    data_1 = data.loc[:(miss_loca-1),:]  # 缺失点之前的数据
    data_2 = data.loc[(miss_loca):,:]  # 缺失点之后的数据
    
    # 计算数据的缺失长度
    miss_len = data['second'][miss_loca]-data['second'][miss_loca-1]-1 # 需要填充的数据个数
    
    # 如果缺失数据在一分钟内，则直接计算长度
    if sign == 'yes':
        
        miss_len = data['second'][miss_loca]-data['second'][miss_loca-1]-1
        data_1 = data.loc[:(miss_loca-1),:]  # 缺失点之前的数据
        data_2 = data.loc[(miss_loca):,:]  # 缺失点之后的数据
    
        col_num = data_1.shape[0]
        
        # 计算三个样本的均值，插入数据
        data_new = list((data.loc[location-1,:]+data.loc[location-3,:]+data.loc[location-2,:])/3)
        
        # 插入数据
        for i in range(miss_len):
            data_1.loc[col_num+i] = data_new # 将数据插入原数据
            
        # 更改秒数
        for i in range(miss_len-1):
            data_1['second'][miss_loca+i] = data['second'][miss_loca-1]+i+1
        
        # 得到处理完一个分割点的数据
        data_comple = data_1.append(data_2)
        
        # 计算处理好的缺失数据的位置
        miss_new = miss_location(data_comple)
    
        
    
    # 如果确实数据不再一分钟内，则将数据填充分为两部分
    else:
        miss_len_1 = 60-data['second'][miss_loca-1]-1
        miss_len_2 = data['second'][miss_loca]
        
        # 计算三个样本的均值，插入数据
        data_new_1 = list((data.loc[location-1,:]+data.loc[location-3,:]+data.loc[location-2,:])/3)
        data_new_2 = list((data.loc[location,:]+data.loc[location+1,:]+data.loc[location+2,:])/3)
        
        col_num = data_1.shape[0]
        
        # 插入数据
        for i in range(miss_len_1):
            data_1.loc[col_num+i] = data_new_1 # 将数据插入原数据
            
        for i in range(miss_len_2-1):
            data_1.loc[col_num+miss_len_1+i] = data_new_2 # 将数据插入原数据
            
        # 更换秒数
        for i in range(miss_len_1-1):
            data_1['second'][miss_loca+i] = data['second'][miss_loca-1]+i+1
        
        for j in range(miss_len_2-1):
            data_1['second'][miss_loca+miss_len_1+1+j] = j
            
        
        # 得到处理完一个分割点的数据
        data_comple = data_1.append(data_2,ignore_index=True) 
        
        # 计算处理好的缺失数据的位置
        miss_new = miss_location(data_comple)


    return data_comple ,miss_new


data_try,miss_new = data_plus(data_ori,miss[0],sign = 'no')





