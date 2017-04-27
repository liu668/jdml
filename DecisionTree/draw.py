# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
def main():
 
    colorList = ['b','g','r','c','m','y','k']
  # # 共用的横坐标
    threadList = [1,2,4,8,10]
  # ���ú�����������������
    plt.xlabel('threads')
    plt.ylabel('concurrent')
     # ͼ�ı���
    plt.title('concurrent test')
     # Ҫ���Ƶ��ߵ��б�
    lines = []
    # ��Ӧ���ߵ�����
    titles = []
    # ��һ���ߵ�������
    dataList1 = [2,5,7,15,30]
    # ���ݺ�����������껭��һ����
    line1 = plt.plot(threadList, dataList1)
    # �����ߵ���ɫ��ȵ�
    plt.setp(line1, color=colorList[0], linewidth=2.0)
    # �ߵ�����
    titles.append('Linux')
    lines.append(line1)
     # ͬ���ڶ�����
    dataList2 = [2,4,6,18,35]
    line2 = plt.plot(threadList, dataList2)
    plt.setp(line2, color=colorList[1], linewidth=2.0)
    titles.append('FreeBSD')
    lines.append(line2)
    plt.legend(lines, titles)
    plt.savefig('C:/Users/liu/Desktop/test.png', dpi=120)
    #�����pdf��,plt.savefig('/home/workspace/test.pdf')
if __name__ == '__main__':
  main()

