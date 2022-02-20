'''
Generate riboseq mapping results for 100AA,90AA and 50AA smORFs.
'''

def assign(infile1,infile2,outfile1,outfile2,outfile3,outfile4,outfile5):
    import gzip
    import lzma

    out1 = gzip.open(outfile1, "wt", compresslevel=1)
    out2 = gzip.open(outfile2, "wt", compresslevel=1)
    out3 = gzip.open(outfile3, "wt", compresslevel=1)
    out4 = gzip.open(outfile4, "wt", compresslevel=1)
    out5 = gzip.open(outfile5, "wt", compresslevel=1)

    riboseq = set()
    smorf = set()
    cluster_90 = {}
    cluster_50 = {}   

    with open (infile1,"rt") as f1:
        for line in f1:
            line = line.strip()
            if line.startswith("smORF"):
                continue
            else:
                linelist = line.split("\t")
                riboseq.add(linelist[0])
            
    with lzma.open(infile2,"rt") as f2:
        for line in f2:
            line = line.strip()
            linelist = line.split("\t")
            if linelist[1] in riboseq:
                smorf.add(linelist[0])
                out1.write(linelist[0]+"\n")
                
    out1.close() 
                
    with lzma.open(infile2,"rt") as f3:
        for line in f3:
            line = line.strip()
            linelist = line.split("\t")
            if linelist[1] != "":
                if linelist[1] in cluster_90.keys():
                    if linelist[0] in smorf: 
                        cluster_90[linelist[1]][0] += 1
                    else:
                        cluster_90[linelist[1]][1] += 1        
                else:
                    cluster_90[linelist[1]] = [0,0]
                    if linelist[0] in smorf: 
                        cluster_90[linelist[1]][0] += 1
                    else:
                        cluster_90[linelist[1]][1] += 1  

            if len(linelist) > 2:
                if linelist[2] in cluster_50.keys():
                    if linelist[0] in smorf: 
                        cluster_50[linelist[2]][0] += 1
                    else:
                        cluster_50[linelist[2]][1] += 1        
                else:
                    cluster_50[linelist[2]] = [0,0]
                    if linelist[0] in smorf: 
                        cluster_50[linelist[2]][0] += 1
                    else:
                        cluster_50[linelist[2]][1] += 1    
    
    for key,value in cluster_90.items():
        out2.write(key+"\t"+str(value[0])+"\t"+str(value[1])+"\t"+str(value[0]/(value[0]+value[1]))+"\n")
    out2.close()

    with gzip.open (outfile2,"rt") as f4:
        for line in f4:
            line = line.strip()
            linelist = line.split("\t")
            if float(linelist[3]) > 0:
                out3.write(linelist[0]+"\n")
    out3.close()

    for key,value in cluster_50.items():
        out4.write(key+"\t"+str(value[0])+"\t"+str(value[1])+"\t"+str(value[0]/(value[0]+value[1]))+"\n")
    out4.close()       

    with gzip.open (outfile4,"rt") as f5:
        for line in f5:
            line = line.strip()
            linelist = line.split("\t")
            if float(linelist[3]) > 0:
                out5.write(linelist[0]+"\n")
    out5.close()

INPUT_FILE_1 = "/riboseq/result/merge/riboseq_result_filter.tsv"
INPUT_FILE_2 = "/data/frozen/all_0.9_0.5_family.tsv.xz"
OUTPUT_FILE_1 = "/riboseq/result/merge/riboseq_100AA.tsv.gz"
OUTPUT_FILE_2 = "/metaproteomes/merge_result/90AA_F_T_rate.tsv.gz"
OUTPUT_FILE_3 = "/metaproteomes/merge_result/metaP_90AA.tsv.gz"
OUTPUT_FILE_4 = "/metaproteomes/merge_result/50AA_F_T_rate.tsv.gz"
OUTPUT_FILE_5 = "/metaproteomes/merge_result/metaP_50AA.tsv.gz"

assign(INPUT_FILE_1,INPUT_FILE_2,OUTPUT_FILE_1,OUTPUT_FILE_2,OUTPUT_FILE_3,OUTPUT_FILE_4,OUTPUT_FILE_5)