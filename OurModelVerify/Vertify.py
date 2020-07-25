# -*- coding: utf-8 -*-
from OurModelVerify import ChunkVerify
from OurModelVerify import ErrorVerify
from OurModelVerify import EveryChunkUnion

class Verify():
    def __init__(self, name):
        self.name = name

    def all_verify(self):
        # 19折交叉检验
        for chunk_number in range(1, 20):
            thread = ChunkVerify.VerifyClass(str(chunk_number) + "号交叉检验法",
                                             chunk_number, "./VerifyOutPut/")
            thread.start()
            thread.join()
        # 归并交叉检验结果
        chunk_union = EveryChunkUnion.EveryChunkUnionClass("./VerifyOutPut/", "./VerifyUnion/")
        chunk_union.union()
        # 计算误差
        error_verify = ErrorVerify.ErrorVerifyClass("./VerifyUnion/ranks_result.csv", "./VerifyError/")
        error_verify.error_verify()

if __name__ == '__main__':
    verify = Verify("合并检验")
    verify.all_verify()