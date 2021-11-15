# Last update: 06-Oct-2021
# Created @Mengmeng Li
# E-mail: mengmeng.li@vu.nl or mengbjfu@126.com
# Institute for Environmental Studies (IVM), VU University Amsterdam
# !!!!!! Please modifiy file pathways accordingly. !!!!!!

import os
import pandas as pd
import numpy as np
import scipy.stats as stats

root_folder = os.path.dirname(os.getcwd())
df_base = pd.read_csv(root_folder + '\\InputData\\InputData.csv')


#-----------------------------------------------------------------#
# This function allocates BU land changes owing to POP change and #
# to BPC change for ten world regions and all regions combined.   #                                 
#-----------------------------------------------------------------#
def ChangesAllocation(FileName_OutputTable):
    df_region_output = pd.DataFrame(columns=['world_region', 'ByPOP_inc', 'ByPOP_dec', 'ByBPC_inc', 'ByBPC_dec'])
    
    for region_name in df_base['world_region'].unique():
        df_region = df_base[df_base['world_region'] == region_name]
        
        PERIOD = [['ByPOP7590', 'ByBPC7590', '1975-1990'],
                  ['ByPOP9000', 'ByBPC9000', '1990-2000'],
                  ['ByPOP0015', 'ByBPC0015', '2000-2015']]
        
        for period in PERIOD:
            df_region_by_pop_incre = df_region[df_region[period[0]] > 0 ]
            region_by_pop_incre = df_region_by_pop_incre[period[0]].sum()
                
            df_region_by_pop_decre = df_region[df_region[period[0]] < 0 ]
            region_by_pop_decre = df_region_by_pop_decre[period[0]].sum()
              
            df_region_by_bpc_incre = df_region[df_region[period[1]] > 0 ]
            region_by_bpc_incre = df_region_by_bpc_incre[period[1]].sum()
                    
            df_region_by_bpc_decre = df_region[df_region[period[1]] < 0 ]
            region_by_bpc_decre = df_region_by_bpc_decre[period[1]].sum()
            
            df_region_output = df_region_output.append({'world_region': region_name,
                                                          'year': period[2], 
                                                          'ByPOP_inc': region_by_pop_incre,
                                                          'ByPOP_dec': region_by_pop_decre,
                                                          'ByBPC_inc': region_by_bpc_incre,
                                                          'ByBPC_dec': region_by_bpc_decre
                                                          }, ignore_index=True)
    
    df_region_output_subset1 = df_region_output[['world_region','ByPOP_inc', 'year']]
    df_region_output_subset1.rename(columns = {'ByPOP_inc':'BUChange'},  inplace=True)
    df_region_output_subset1.loc[:, 'By'] = 'A-POP'
    
    df_region_output_subset2 = df_region_output[['world_region','ByBPC_inc', 'year']]
    df_region_output_subset2.rename(columns = {'ByBPC_inc':'BUChange'},  inplace=True)
    df_region_output_subset2.loc[:, 'By'] = 'B-BPC'
    
    df_inc = df_region_output_subset1.append(df_region_output_subset2)
    df_inc.loc[:, 'type'] = 'positive'
    
    df_region_output_subset3 = df_region_output[['world_region','ByPOP_dec', 'year']]
    df_region_output_subset3.rename(columns = {'ByPOP_dec':'BUChange'},  inplace=True)
    df_region_output_subset3.loc[:, 'By'] = 'A-POP'
    
    df_region_output_subset4 = df_region_output[['world_region','ByBPC_dec', 'year']]
    df_region_output_subset4.rename(columns = {'ByBPC_dec':'BUChange'},  inplace=True)
    df_region_output_subset4.loc[:, 'By'] = 'B-BPC'
    
    df_dec = df_region_output_subset3.append(df_region_output_subset4)
    df_dec.loc[:, 'type'] = 'negative'
    
    df_world_region = df_inc.append(df_dec)
    df_world_region.to_csv(root_folder + '\\data\\' + FileName_OutputTable)
    
    df_world_region_Extra = df_world_region.groupby(['year', 'By', 'type'])['BUChange'].sum()
    df_world_region_Extra.to_csv(root_folder + '\\data\\' + FileName_OutputTable[:-4] + '_Extra.csv')

# Allocation strategy option 01:
df_base['ByPOP7590'] = df_base.POP7590 * df_base.bpc1975
df_base['ByPOP9000'] = df_base.POP9000 * df_base.bpc1990
df_base['ByPOP0015'] = df_base.POP0015 * df_base.bpc2000
df_base['ByBPC7590'] = df_base.BPC7590 * df_base.p1990
df_base['ByBPC9000'] = df_base.BPC9000 * df_base.p2000
df_base['ByBPC0015'] = df_base.BPC0015 * df_base.p2015
ChangesAllocation('ChangesAllocation_option_01.csv')

# Allocation strategy option 02
df_base['ByPOP7590'] = df_base.POP7590 * df_base.bpc1990
df_base['ByPOP9000'] = df_base.POP9000 * df_base.bpc2000
df_base['ByPOP0015'] = df_base.POP0015 * df_base.bpc2015
df_base['ByBPC7590'] = df_base.BPC7590 * df_base.p1975
df_base['ByBPC9000'] = df_base.BPC9000 * df_base.p1990
df_base['ByBPC0015'] = df_base.BPC0015 * df_base.p2000
ChangesAllocation('ChangesAllocation_option_02.csv')

# Allocation strategy option 03
df_base['ByPOP7590'] = np.where((df_base.POP7590 >=0), df_base.POP7590 * df_base.bpc1990, df_base.POP7590 * df_base.bpc1975)
df_base['ByPOP9000'] = np.where((df_base.POP9000 >=0), df_base.POP9000 * df_base.bpc2000, df_base.POP9000 * df_base.bpc1990)
df_base['ByPOP0015'] = np.where((df_base.POP0015 >=0), df_base.POP0015 * df_base.bpc2015, df_base.POP0015 * df_base.bpc2000)
df_base['ByBPC7590'] = np.where((df_base.POP7590 >=0), df_base.BPC7590 * df_base.p1975, df_base.BPC7590 * df_base.p1990)
df_base['ByBPC9000'] = np.where((df_base.POP9000 >=0), df_base.BPC9000 * df_base.p1990, df_base.BPC9000 * df_base.p2000)
df_base['ByBPC0015'] = np.where((df_base.POP0015 >=0), df_base.BPC0015 * df_base.p2000, df_base.BPC0015 * df_base.p2015)
ChangesAllocation('ChangesAllocation_option_03.csv')

# Suggested by Reviewer
# Allocation strategy option 04:
df_base['ByPOP7590'] = np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#11
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), df_base.b1990 - df_base.b1975,#12
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), 0,#13
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 >= 1), df_base.b1990 - df_base.b1975,#14
                                
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#21
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), df_base.b1990 - df_base.b1975,#22
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), 0,#23
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 > 0)&(df_base.p1990 >= 0), df_base.b1990 - df_base.b1975,#24                                  
                                
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), 0,#31
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), 0,#32
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), 0,#33
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 >= 1), df_base.b1990 - df_base.b1975,#34

                       np.where((df_base.b1975 > 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#41
                       np.where((df_base.b1975 > 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), 0,#42
                       np.where((df_base.b1975 > 0)&(df_base.p1975 >= 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#43
                                (df_base.b1990 - df_base.b1975) * (np.log(df_base.p1990/df_base.p1975))/(np.log(df_base.b1990/df_base.b1975)))))))))))))))))#44 

df_base['ByPOP9000'] = np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#11
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), df_base.b2000 - df_base.b1990,#12
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), 0,#13
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 >= 1), df_base.b2000 - df_base.b1990,#14
                                
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#21
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), df_base.b2000 - df_base.b1990,#22
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), 0,#23
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 > 0)&(df_base.p2000 >= 0), df_base.b2000 - df_base.b1990,#24                                  
                                
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), 0,#31
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), 0,#32
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), 0,#33
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 >= 1), df_base.b2000 - df_base.b1990,#34

                       np.where((df_base.b1990 > 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#41
                       np.where((df_base.b1990 > 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), 0,#42
                       np.where((df_base.b1990 > 0)&(df_base.p1990 >= 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#43
                                (df_base.b2000 - df_base.b1990) * (np.log(df_base.p2000/df_base.p1990))/(np.log(df_base.b2000/df_base.b1990)))))))))))))))))#44 

df_base['ByPOP0015'] = np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#11
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), df_base.b2015 - df_base.b2000,#12
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), 0,#13
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 >= 1), df_base.b2015 - df_base.b2000,#14
                                
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#21
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), df_base.b2015 - df_base.b2000,#22
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), 0,#23
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 > 0)&(df_base.p2015 >= 0), df_base.b2015 - df_base.b2000,#24                                  
                                
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), 0,#31
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), 0,#32
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), 0,#33
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 >= 1), df_base.b2015 - df_base.b2000,#34

                       np.where((df_base.b2000 > 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#41
                       np.where((df_base.b2000 > 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), 0,#42
                       np.where((df_base.b2000 > 0)&(df_base.p2000 >= 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#43
                                (df_base.b2015 - df_base.b2000) * (np.log(df_base.p2015/df_base.p2000))/(np.log(df_base.b2015/df_base.b2000)))))))))))))))))#44 

df_base['ByBPC7590'] = np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), 0,#11
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), 0,#12
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#13
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 >= 1), 0,#14
                                
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), 0,#21
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), 0,#22
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#23
                       np.where((df_base.b1975 <= 0)&(df_base.p1975 >= 1)&(df_base.b1990 > 0)&(df_base.p1990 >= 1), 0,#24
                                  
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#31
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), df_base.b1990 - df_base.b1975,#32
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), df_base.b1990 - df_base.b1975,#33
                       np.where((df_base.b1975 > 0)&(df_base.p1975 < 1)&(df_base.b1990 > 0)&(df_base.p1990 >= 1), 0,#34
                                
                       np.where((df_base.b1975 > 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 < 1), 0,#41
                       np.where((df_base.b1975 > 0)&(df_base.p1975 >= 1)&(df_base.b1990 <= 0)&(df_base.p1990 >= 1), df_base.b1990 - df_base.b1975,#42
                       np.where((df_base.b1975 > 0)&(df_base.p1975 >= 1)&(df_base.b1990 > 0)&(df_base.p1990 < 1), 0,#43
                                (df_base.b1990 - df_base.b1975) * (1-(np.log(df_base.p1990/df_base.p1975))/(np.log(df_base.b1990/df_base.b1975))))))))))))))))))#44 

df_base['ByBPC9000'] = np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), 0,#11
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), 0,#12
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#13
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 >= 1), 0,#14
                                
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), 0,#21
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), 0,#22
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#23
                       np.where((df_base.b1990 <= 0)&(df_base.p1990 >= 1)&(df_base.b2000 > 0)&(df_base.p2000 >= 1), 0,#24
                                  
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#31
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), df_base.b2000 - df_base.b1990,#32
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), df_base.b2000 - df_base.b1990,#33
                       np.where((df_base.b1990 > 0)&(df_base.p1990 < 1)&(df_base.b2000 > 0)&(df_base.p2000 >= 1), 0,#34
                                
                       np.where((df_base.b1990 > 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 < 1), 0,#41
                       np.where((df_base.b1990 > 0)&(df_base.p1990 >= 1)&(df_base.b2000 <= 0)&(df_base.p2000 >= 1), df_base.b2000 - df_base.b1990,#42
                       np.where((df_base.b1990 > 0)&(df_base.p1990 >= 1)&(df_base.b2000 > 0)&(df_base.p2000 < 1), 0,#43
                                (df_base.b2000 - df_base.b1990) * (1-(np.log(df_base.p2000/df_base.p1990))/(np.log(df_base.b2000/df_base.b1990))))))))))))))))))#44 
df_base['ByBPC0015'] = np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), 0,#11
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), 0,#12
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#13
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 >= 1), 0,#14
                                
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), 0,#21
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), 0,#22
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#23
                       np.where((df_base.b2000 <= 0)&(df_base.p2000 >= 1)&(df_base.b2015 > 0)&(df_base.p2015 >= 1), 0,#24
                                  
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#31
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), df_base.b2015 - df_base.b2000,#32
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), df_base.b2015 - df_base.b2000,#33
                       np.where((df_base.b2000 > 0)&(df_base.p2000 < 1)&(df_base.b2015 > 0)&(df_base.p2015 >= 1), 0,#34
                                
                       np.where((df_base.b2000 > 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 < 1), 0,#41
                       np.where((df_base.b2000 > 0)&(df_base.p2000 >= 1)&(df_base.b2015 <= 0)&(df_base.p2015 >= 1), df_base.b2015 - df_base.b2000,#42
                       np.where((df_base.b2000 > 0)&(df_base.p2000 >= 1)&(df_base.b2015 > 0)&(df_base.p2015 < 1), 0,#43
                                (df_base.b2015 - df_base.b2000) * (1-(np.log(df_base.p2015/df_base.p2000))/(np.log(df_base.b2015/df_base.b2000))))))))))))))))))#44 
ChangesAllocation('ChangesAllocation_option_04.csv')


# Pre-process the data for further analysis
df_table = df_base[['d_code', 'b1975', 'b1990', 'b2000', 'b2015',
                   'p1975', 'p1990', 'p2000', 'p2015',
                   'c_code', 'T7590', 'T9000', 'T0015',
                   'region_type', 'world_region']]

df_table75 = df_table[['d_code', 'b1975', 'b1990', 'p1975', 'p1990', 'c_code', 'T7590', 'region_type', 'world_region']]
df_table75.rename(columns=
                      {'b1975': 'BU_start',
                       'b1990': 'BU_end',
                       'p1975': 'POP_start',
                       'p1990': 'POP_end',
                       'region_type': 'region_type',
                       'world_region': 'world_region',
                       'T7590': 'tj'}, inplace = True)
df_table75.loc[:, 'Period'] = 'P1975-1990'

df_table90 = df_table[['d_code', 'b1990', 'b2000', 'p1990', 'p2000', 'c_code', 'T9000', 'region_type', 'world_region']]
df_table90.rename(columns=
                      {'b1990': 'BU_start',
                       'b2000': 'BU_end',
                       'p1990': 'POP_start',
                       'p2000': 'POP_end',
                       'region_type': 'region_type',
                       'world_region': 'world_region',
                       'c_code': 'c_code',
                       'T9000': 'tj'}, inplace = True)
df_table90.loc[:, 'Period'] = 'P1990-2000'

df_table00 = df_table[['d_code', 'b2000', 'b2015', 'p2000', 'p2015', 'c_code', 'T0015', 'region_type', 'world_region']]
df_table00.rename(columns=
                      {'b2000': 'BU_start',
                       'b2015': 'BU_end',
                       'p2000': 'POP_start',
                       'p2015': 'POP_end',
                       'region_type': 'region_type',
                       'world_region': 'world_region',
                       'c_code': 'c_code',
                       'T0015': 'tj'}, inplace = True)
df_table00.loc[:, 'Period'] = 'P2000-2015'

df_table_new = pd.concat([df_table75, df_table90, df_table00])


#-----------------------------------------------------------------#
# Table 01. Built-up land and population for different urban land #
# change trajectories as well as their changes over time.         #
#-----------------------------------------------------------------#
df_table_1 = df_table_new[['Period', 'tj', 'BU_start', 'BU_end', 'POP_start', 'POP_end']]
Trajectory_Table = df_table_1.groupby(['Period', 'tj']).sum()
Trajectory_Table['BU_change'] = Trajectory_Table['BU_end'] - Trajectory_Table['BU_start']
Trajectory_Table['POP_change'] = Trajectory_Table['POP_end'] - Trajectory_Table['POP_start']
Trajectory_Table.to_csv(root_folder + '\\data\\Table01_Trajectory_statistics.csv')
Trajectory_Table_count = df_table_new[['Period', 'tj', 'BU_start']].groupby(['Period', 'tj']).count()
Trajectory_Table_count.to_csv(root_folder + '\\data\\Table01_Trajectory_statistics_count.csv')

df_table_1_t = df_table_1
df_table_1_t['BU_change'] = df_table_1_t['BU_end'] - df_table_1_t['BU_start']
df_table_1_t['POP_change'] = df_table_1_t['POP_end'] - df_table_1_t['POP_start']


my_PeriodList = ['P1975-1990', 'P1990-2000', 'P2000-2015']
my_TrajectoryList = [1, 2, 3, 5, 6, 9]
myPropertyList = ['BU_start', 'BU_change', 'POP_start', 'POP_change']

print('-------Trajectory--------')
for myProperty in myPropertyList:
    print(myProperty)
    for my_Period in my_PeriodList:
        print(my_Period)
        df_table_period = df_table_1_t[df_table_1_t['Period'] == my_Period]
        for my_Trajectory in my_TrajectoryList:
                df_part = df_table_period[df_table_period['tj'] == my_Trajectory]
                df_all = df_table_period
                print(my_Trajectory, stats.ttest_ind(df_part[myProperty], df_all[myProperty]).pvalue)


#-----------------------------------------------------------------#
# Table 02. Built-up land and population for regions in different #
# urbanization classes as well as their changes over time.        #
#-----------------------------------------------------------------#
df_table_23 = df_table_new[['Period', 'region_type', 'BU_start', 'BU_end', 'POP_start', 'POP_end']]
region_type_Table = df_table_23.groupby(['Period', 'region_type']).sum()
region_type_Table['BU_change'] = region_type_Table['BU_end'] - region_type_Table['BU_start']
region_type_Table['POP_change'] = region_type_Table['POP_end'] - region_type_Table['POP_start']
region_type_Table.to_csv(root_folder + '\\data\\Table02&03_Region_type.csv')


df_table_23_t = df_table_23
df_table_23_t['BU_change'] = df_table_23_t['BU_end'] - df_table_23_t['BU_start']
df_table_23_t['POP_change'] = df_table_23_t['POP_end'] - df_table_23_t['POP_start']

my_PeriodList = ['P1975-1990', 'P1990-2000', 'P2000-2015']
my_RegionTypeList = [0, 1, 2, 3, 4]
myPropertyList = ['BU_start', 'BU_change', 'POP_start', 'POP_change']

print('-------Region Type--------')
for myProperty in myPropertyList:
    print(myProperty)
    for my_Period in my_PeriodList:
        print(my_Period)
        df_table_period = df_table_23_t[df_table_23_t['Period'] == my_Period]
        for my_RegionType in my_RegionTypeList:
                df_part = df_table_period[df_table_period['region_type'] == my_RegionType]
                df_all = df_table_period
                print(my_RegionType, stats.ttest_ind(df_part[myProperty], df_all[myProperty]).pvalue)


print('------For Table 03-------')
df_table_3_t = df_base[['region_type','bpc1975', 'bpc1990', 'bpc2000', 'BU75', 'BU90', 'BU00', 'POP75', 'POP90', 'POP00', 'BPC75', 'BPC90', 'BPC00']]
for myProperty in ['bpc1975', 'bpc1990', 'bpc2000', 'BU75', 'BU90', 'BU00', 'POP75', 'POP90', 'POP00', 'BPC75', 'BPC90', 'BPC00']:
    print(myProperty)
    for my_RegionType in my_RegionTypeList:
        df_part = df_table_3_t[df_table_3_t['region_type'] == my_RegionType]
        df_all = df_table_3_t
        print(my_RegionType, stats.ttest_ind(df_part[myProperty], df_all[myProperty]).pvalue)

        
#-----------------------------------------------------------------#
# Fig.03_Table Trajectory map.                                    #
#-----------------------------------------------------------------#
df_Fig03_Table = df_base[['FID', 'T7590', 'T9000', 'T0015']]
df_Fig03_Table.to_csv(root_folder + '\\data\\Fig03_Table.csv')


#-----------------------------------------------------------------#
# Fig.04S03 Number of regions following specific trajectories.    #
#-----------------------------------------------------------------#
df_table_23 = df_table_new[['Period', 'region_type', 'tj']]
df_table_23.loc[:, 'NoOfRegion'] = 1
df_Fig04S03_Table = df_table_23.groupby(['Period', 'region_type', 'tj']).sum()
df_Fig04S03_Table = df_Fig04S03_Table.pivot_table(index = ['Period', 'region_type'], columns = ['tj'], values = 'NoOfRegion')
df_Fig04S03_Table.to_csv(root_folder + '\\data\\Fig04&S03_Table.csv')


#-----------------------------------------------------------------#
# Within-country variation for HUDI calculation                   #
#-----------------------------------------------------------------#
df_WithinCountry = pd.DataFrame(columns=['a_code', 'NoRegion', 'Period', 'ByPOP_inc', 'ByPOP_dec', 'ByBPC_inc', 'ByBPC_dec',
                                         'HUDI_POP', 'HUDI_BPC'])

for country_id in df_base['a_code'].unique():
    df_country = df_base[df_base['a_code'] == country_id]
    
    PERIOD = [['ByPOP7590', 'ByBPC7590', '75-90'],
              ['ByPOP9000', 'ByBPC9000', '90-00'],
              ['ByPOP0015', 'ByBPC0015', '00-15']]
    
    for period in PERIOD:
                
        df_country_by_pop_incre = df_country[df_country[period[0]] > 0 ]
        country_by_pop_incre = df_country_by_pop_incre[period[0]].sum()
            
        df_country_by_pop_decre = df_country[df_country[period[0]] < 0 ]
        country_by_pop_decre = df_country_by_pop_decre[period[0]].sum()
          
        df_country_by_bpc_incre = df_country[df_country[period[1]] > 0 ]
        country_by_bpc_incre = df_country_by_bpc_incre[period[1]].sum()
                
        df_country_by_bpc_decre = df_country[df_country[period[1]] < 0 ]
        country_by_bpc_decre = df_country_by_bpc_decre[period[1]].sum()
        
        HUDI_POP_country = (country_by_pop_incre + country_by_pop_decre) / max(country_by_pop_incre, abs(country_by_pop_decre))
        HUDI_BPC_country = (country_by_bpc_incre + country_by_bpc_decre) / max(country_by_bpc_incre, abs(country_by_bpc_decre))
            
        df_WithinCountry = df_WithinCountry.append({
                        'a_code': country_id,
                        'NoRegion': len(df_country),
                        'Period': period[2], 
                        'ByPOP_inc': country_by_pop_incre,
                        'ByPOP_dec': country_by_pop_decre,
                        'ByBPC_inc': country_by_bpc_incre,
                        'ByBPC_dec': country_by_bpc_decre,
                        'HUDI_POP': HUDI_POP_country,
                        'HUDI_BPC': HUDI_BPC_country
                    }, ignore_index=True)

df_WithinCountry.to_csv(root_folder + '\\data\\HUDI_WithinCountry.csv')


#-----------------------------------------------------------------#
# Tables S02 and S03 for ten world regions                        #
#-----------------------------------------------------------------#
df_for_TabS23 = df_table_new[['Period', 'world_region', 'BU_start', 'BU_end', 'POP_start', 'POP_end']]
df_for_TabS23_sum = df_for_TabS23.groupby(['Period', 'world_region']).sum()
df_for_TabS23_sum['BU_change'] = df_for_TabS23_sum['BU_end'] - df_for_TabS23_sum['BU_start']
df_for_TabS23_sum['POP_change'] = df_for_TabS23_sum['POP_end'] - df_for_TabS23_sum['POP_start']
df_for_TabS23_sum.to_csv(root_folder + '\\data\\TableS02&03_World_region.csv')


df_table_S23_t = df_for_TabS23
df_table_S23_t['BU_change'] = df_table_S23_t['BU_end'] - df_table_S23_t['BU_start']
df_table_S23_t['POP_change'] = df_table_S23_t['POP_end'] - df_table_S23_t['POP_start']

my_PeriodList = ['P1975-1990', 'P1990-2000', 'P2000-2015']
my_WorldRegionList = ['CanUSA', 'China', 'Europe', 'India', 'LatinAmerica', 'MEandNAF',
                      'Oceania', 'RusCA', 'SEA', 'SSAfrica']
myPropertyList = ['BU_start', 'BU_change', 'POP_start', 'POP_change']

print('-------World Region Table S02--------')
for myProperty in myPropertyList:
    print(myProperty)
    for my_Period in my_PeriodList:
        print(my_Period)
        df_table_period = df_table_S23_t[df_table_S23_t['Period'] == my_Period]
        for my_WorldRegion in my_WorldRegionList:
                df_part = df_table_period[df_table_period['world_region'] == my_WorldRegion]
                df_all = df_table_period
                print(my_WorldRegion, len(df_part), stats.ttest_ind(df_part[myProperty], df_all[myProperty]).pvalue)

print('------For Table S03-------')
df_table_S3_t = df_base[['world_region','bpc1975', 'bpc1990', 'bpc2000', 'BU75', 'BU90', 'BU00', 'POP75', 'POP90', 'POP00', 'BPC75', 'BPC90', 'BPC00']]
for myProperty in ['bpc1975', 'bpc1990', 'bpc2000', 'BU75', 'BU90', 'BU00', 'POP75', 'POP90', 'POP00', 'BPC75', 'BPC90', 'BPC00']:
    print(myProperty)
    for my_WorldRegion in my_WorldRegionList:
        df_part = df_table_S3_t[df_table_S3_t['world_region'] == my_WorldRegion]
        df_all = df_table_S3_t
        print(my_WorldRegion, stats.ttest_ind(df_part[myProperty], df_all[myProperty]).pvalue)
