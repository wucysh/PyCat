import logging
import os


def accSum(n):
    """
    叠加函数 ：从0进行叠加
    :param n:
    :return:
    """
    sum = 0
    for i in range(1, n):  # [1,n+1)
        print(i, end='+')
        sum += i
    print('=', sum)
    return sum


def getrate(tol, months, sxf):
    # 每月还款本金
    month_amt = tol / months
    # 6300 / (140000 * 12 * 30 - (0~11) * 11666.67 * 12 * 30)
    rate = (sxf * months * 10000) / (tol * 30 * months - accSum(months) * month_amt * 30)
    print('贷款：' + str(tol), '等额还款' + str(months), '期')
    print('每期还款：', '{:.2f}'.format(month_amt + sxf))
    print('每期手续费：' + str(sxf), '总计:' + str(sxf * months))
    print('合计一万每天：', '{:.2f}'.format(rate), '元')


if __name__ == "__main__":
    """
    主函数
    """
    # getrate(140000, 12, 525)
    # getrate(140000, 18, 525)
    getrate(140000, 24, 525)
    # getrate(100000, 12*5, 30555/(12*5))
    # getrate(100000, 36, 380)
