import pandas as pd
import re

def get_table_cut(filename_read,filename_write):
  data = pd.read_csv(filename_read, encoding='utf8',low_memory=False)
  list1 = [data['产品型号_G'][i] for i in range(0, len(data))]
  list1 = list(set(list1))#去除掉重复列
  max_place=[]
  for model in list1:
     df=data.loc[data['产品型号_G']==model].astype(str)
     item,item1=[],[]
     df=df.replace(to_replace=re.compile(r'.*nan.*'), value='0')#把NAN变成0
     for i in range(0,len(df)):
         x=df.index
         total = int('{}{}{:02d}{:02d}'.format(int(float(df['公告批次_G'][x[i]])), int(float(df['推荐目录颁布年份_X'][x[i]])),
            int(float(df['推荐目录颁布批次_X'][x[i]])),int(float(df['批次_M'][x[i]]))))
         item.append((total,x[i]))
         item1.append(total)
     dict1=dict(item)
     try:
        max_place.append(dict1[max(item1)])
     except  Exception as e:
          print(dict1)
  data_table=data.loc[max_place]
  data_table=data_table.set_index('企业名称_G')
  data_table.to_csv(filename_write)
  
def main():
    filenames=['table_merge_ev.csv','table_merge_phev.csv','table_merge_ke_ev.csv','table_merge_ke_hev.csv']
    for filename in filenames:
        get_table_cut('worktable/'+filename, 'worktable/'+filename[:-4]+'_cut'+'.csv')

if __name__ == '__main__':
    main()

