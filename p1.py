
# coding: utf-8

# # 亲和性分析示例
# 
# 亲和性分析是根据样本个体之间的相似度，确定它们关系的亲疏。
# 比如：向网站用户提供多样化的服务或定向投放广告
# 
# 亲和性还有多种测量方法，比如，统计两件商品一起出售的概率，或者统计用户购买了商品1后再购买商品2的比率。
# 
# 下面具体分析下如何计算个体之间的相似度。
# 
# 场景：
# 一个人去超市买东西，买了面包后又买了牛奶。
# 作为数据挖掘入门性质的例子，我们希望得到下面这样的规则：
# “如果一个人买了商品X,那么他可能购买Y”
# 
# 
# 下面我们导入具体的数据集

# In[23]:


import numpy as np
dataset_filename = "dataset.txt"
datas = np.loadtxt(dataset_filename)
n_samples, n_features = data.shape
print(n_samples) # 行数
print(n_features) # 列数


# dataset.txt的文件请从后面提供的git地址上下载

# In[24]:


print(datas[:5])


# 每行代表用户每次购买的5个商品
# 假设每列分别代表面包、牛奶、奶酪、苹果和香蕉
# 比如第一行是[0. 0. 1. 1. 1.]
# 代表用户买了奶酪、苹果和香蕉，没有买面包、牛奶
# 1-> 表示买了该商品
# 0-> 表示没有买该商品

# In[73]:


products_name = ["面包", "牛奶", "奶酪", "苹果", "香蕉"]


# ## 实现简单的排序规则
# 
# 如果要找出"如果一个人买了商品X,那么他可能购买Y"这样的规则。
# 简单的办法就是找出数据集中所有同时购买两件商品的情况，找到规则后，我们还需要判断规则的优劣，最后选择最优的。
# 
# 规则的优劣有多种衡量方法，常用的方法有“支持度”和“置信度”
# 
# 支持度指数据集里面规则有效的次数，统计起来很简单。
# 有时候，还需要对支持度进行规范化，即再除以规则有效的总数量。
# 我们这里只简单统计规则有效的次数。
# 
# 支持度衡量的是给定规则有效的比例，而置信度衡量的则是规则有效准确率，即符合给定条件(即规则的“如果”语句所表示的前提条件)的所有规则里，跟当前规则结论一致的比例有多大。
# 计算方法为首先统计当前规则的出现次数，再用它来除以条件(“如果”语句)相同的规则数量
# 
# 如下面的代码所示，通过判断交易数据中data[3]的值，就能知道一个顾客是否买了苹果。 这里，data表示一条交易信息，也就是数据集里的一行数据。

# In[25]:


purchase_apple_sum = 0 # 购买苹果的人数
for data in datas:
    if data[3] == 1: # 购买了苹果
        purchase_apple_sum += 1 # 计算购买了苹果的人数
        
print("{0}人买了苹果".format(purchase_apple_sum))


# In[28]:


'''
有多少人买了苹果有买了香蕉呢
'''
valid_rule = 0 # 符合规则的有效次数
invalid_rule = 0 # 不符合规则的有效次数
purchase_apple_not_banana_num = 0
for data in datas:
    if data[3] == 1: # 购买了苹果
        if data[4] == 1: # 购买了香蕉
            valid_rule += 1 # 计算购买苹果和香蕉的人数
        else:
            invalid_rule += 1 # 计算购买苹果没有购买香蕉的人数
print("{0}人同时购买了苹果和香蕉".format(purchase_apple_and_banana_num))
print("{0}人只购买了苹果没有购买香蕉".format(purchase_apple_not_banana_num))


# In[31]:


'''
现在有了所有需要的数据，我们就可以计算支持度和置信度
'''
# 支持度就是 符合规则有效的次数
support_degree = valid_rule
# 置信度
confidence_degree = valid_rule / purchase_apple_sum
print("支持度是{0}, 置信度是{1:0.3f}".format(support_degree, confidence_degree))
# 置信度可以用百分比来表示
print("置信度的百分比是{0:0.1f}%".format(confidence_degree * 100))


# 为了计算所有规则的置信度和支持度，首先创建一个字典，用来存放计算结果。
# 需要统计的量有
# 1、有效规则
# 2、无效规则
# 3、条件相同的规则数量

# In[57]:


'''
对于上面的符合要求的，即同时购买了苹果和香蕉的标识符合我们的规则，反之不符合我们的规则，按照此逻辑我们找出所有有效规则
'''
from collections import defaultdict
valid_rules = defaultdict(int) # 有效规则
invalid_rules = defaultdict(int) # 无效规则
num_occurances = defaultdict(int) # 规则数量

for data in datas:
    for fruit in range(n_features):
        # 首先检查个体是否符合规则【购买的规则，没有购买的就直接跳过】
        if data[fruit] == 0: # 不符合规则，继续下一个循环 
            continue
        num_occurances[fruit] += 1 # 符合规则加1
        
        for also_fruit in range(n_features):
            if fruit == also_fruit: # 跳过不符合要求的，即我们想要的是买了x水果又买了y水果，而不是买了x水果又买了x水果
                continue
            if data[also_fruit] == 1:
                valid_rules[(fruit, also_fruit)] += 1
                
            else:
                invalid_rules[(fruit, also_fruit)] += 1
                
support_degrees = valid_rules
confidence_degrees = defaultdict(float)
for fruit, also_fruit in valid_rules.keys():
    confidence_degrees[(fruit, also_fruit)] = valid_rules[(fruit, also_fruit)] / num_occurances[fruit]
    


# In[60]:


for fruit, also_fruit in confidence_degrees:
    fruit_name = products_name[fruit]
    also_fruit_name = products_name[also_fruit]
    print("规则: 如果一个人买了商品【{0}】，那么他可能买商品【{1}】".format(fruit_name, also_fruit_name))
    print(" - 置信度是: {0:.3f}".format(confidence_degrees[(fruit, also_fruit)]))
    print(" - 支持度是: {0}".format(support_degrees[(fruit, also_fruit)]))


# In[63]:


def print_rule(fruit, also_fruit, support_degrees, confidence_degrees, products_name):
    fruit_name = products_name[fruit]
    also_fruit_name = products_name[also_fruit]
    print("规则: 如果一个人买了商品【{0}】，那么他可能买商品【{1}】".format(fruit_name, also_fruit_name))
    print(" - 置信度是: {0:.3f}".format(confidence_degrees[(fruit, also_fruit)]))
    print(" - 支持度是: {0}".format(support_degrees[(fruit, also_fruit)]))
    
print_rule(1, 3, support_degrees, confidence_degrees, products_name)


# ## 排序找出最佳规则
# 
# 我们上面已经拿到了所有有效规则及对应的置信度和支持度，为了找出最佳规则，我们还需要根据支持度和置信度对规则进行排序。
# 
# 为了找出支持度最高的规则，首先对支持度字典进行排序。
# 

# In[66]:


# 排序支持度
from pprint import pprint
pprint(list(support_degrees.items()))


# In[68]:


# 使用itemgetter() 类作为键，这样就可以对嵌套列表进行排序
from operator import itemgetter
# itemgetter(1)表示以字典各元素的值(这里为 支持度)作为排序依据，reverse=True表示降序排列。
sorted_support_degrees = sorted(support_degrees.items(), key=itemgetter(1), reverse=True)
print(sorted_support_degrees)


# In[69]:


# 排序完成之后就可以输出支持度最高的前5条
for i in range(5):
    print("规则: #{0}".format(i))
    fruit, also_fruit = sorted_support_degrees[i][0]
    print_rule(fruit, also_fruit, support_degrees, confidence_degrees, products_name)


# In[71]:


'''
同理我们还可以输出置信度最高的规则，首先对置信度进行排序
'''
sorted_confidence_degrees = sorted(confidence_degrees.items(), key=itemgetter(1), reverse=True)
print(sorted_confidence_degrees)


# In[72]:


# 排序完成之后就可以输出置信度最高的前5条
for i in range(5):
    print("规则: #{0}".format(i))
    fruit, also_fruit = sorted_confidence_degrees[i][0]
    print_rule(fruit, also_fruit, support_degrees, confidence_degrees, products_name)


# 从排序结果来看，“顾客买苹果，也会买奶酪”和“顾客买奶酪，也会买香蕉”，这两条规则的支持度和置信度都很高。
# 超市经理可以根据这些规则来调整商品摆放位置。
# 例如，如果本周苹果促销，就在旁边摆上奶酪。
# 但是香蕉和奶酪同时搞促销就没有多大意义了，因为我们发现购买奶酪的顾客中，接近66%的人即使不搞促销也会买香蕉——即使搞促销，也不会给销量带来多大提升
