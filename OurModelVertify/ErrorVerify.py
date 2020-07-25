# -*- coding: utf-8 -*-
import os
import csv

class ErrorVerifyClass:
    def __init__(self, source, output):
        self.source = source
        self.output = output
        self.result = []

        if(not os.path.exists(self.output)):
            os.mkdir(self.output)

    def error_verify(self):
        lines = csv.reader(open(self.source,'r', encoding="utf-8"))

        border = 10
        count = 0
        valid_count = 0

        for line in lines:
            count += 1
            temp = [line[0], line[1]]
            origin = float(line[2])
            higher_error = 0
            lower_error = 0
            for item in line[3:]:
                error = float(item) - origin
                if(error < 0):
                    if(lower_error > error):
                        lower_error = error
                else:
                    if(higher_error < error):
                        higher_error = error
            abs_error = max(abs(higher_error), abs(lower_error))
            # if(abs_error <= border):
            #     valid_count += 1
            if( (higher_error - lower_error) < border * 2):
                valid_count += 1
            temp.extend([higher_error, lower_error, abs_error])
            self.result.append(temp)

        with open(self.output + "error_verify.csv", 'w',encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', "category", "higher_error", "lower_error", "abs_error"])
            for line in self.result:
                writer.writerow(line)
        print("有 %.2f " %(valid_count / count * 100.0) + "%的用户误差区间不超过 " + str(border * 2) +" %.")

if __name__ == '__main__':
    error_verify = ErrorVerifyClass("./VerifyUnion/ranks_result.csv", "./VerifyError/")
    error_verify.error_verify()