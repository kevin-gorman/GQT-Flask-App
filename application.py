from __future__ import print_function
import os
import sys
import boto3
import subprocess
from flask import Flask, render_template, request, url_for, Response, redirect
files = ['ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr10.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr11.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr13.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr14.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr15.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr16.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr20.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr3.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr4.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr5.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr6.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr7.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr8.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr9.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.bcf.gqt', 'ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.bcf.gqt', 'ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.bcf.gqt', 'ALL.chrY.phase3_integrated_v2a.20130502.genotypes.bcf.gqt']
chs = ['ch1', 'ch10', 'ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch2', 'ch20', 'ch21', 'ch22' 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', ]
application = Flask(__name__)
first = True
'''
@application.route("/")
def home():
    return render_template("home.html")
'''
@application.route("/")   
@application.route("/about")
def about():
    #params = [i,d,c,v,t,B,O,V,G,p1,g1,p2,g2]
    '''
    gqt query -i <bcf/vcf or gqt file> \
                   -d <ped database file> \
                   -c only print number of resulting variants \
                   -v print genotypes (from the source bcf/vcf)\
                   -t tmp direcory name for remote files (default ./)
                   -B <bim file> (opt.)\
                   -O <off file> (opt.)\
                   -V <vid file> (opt.)\
                   -G <gqt file> (opt.)\
                   -p <population query 1> \
                   -g <genotype query 1> \
                   -p <population query 2> \
                   -g <genotype query 2> \
    '''
    #req_data = request.get_json()
    return render_template("about.html")
    
@application.route("/query", methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    form = request.url
    index = form.find("query")
    form = form[index + 6:]
    form = form.replace("&", " ")
    form = form.replace("=", " ")
    form = form.replace("+", " ")
    form = form.replace("%3C", "<")
    form = form.replace("%3D", "=")
    form = form.replace("%3E", ">")
    form = form.split()
    if request.method == 'GET' and not (form == []): #this block is only entered when the form is submitted
        #os.chdir('/tmp')
        funlist = request.form.getlist("Function")
        poplist = request.form.getlist("P")
        #pop1 = request.form.getlist("pop1")
        #pop2 = request.form.getlist("pop2")
        #pop3 = request.form.getlist("pop3")
        #pop = request.form.getlist("pop")
        #res = [pop1,pop2,pop3]
        #res = pop
        #form = request.url
        #res = ['/home/ec2-user/environment/python-gqt/lib/gqt/bin/gqt', 'query', "-i", "http://gqt-files.s3.amazonaws.com/chr11.11q14.3.bcf.gqt", "-d", "http://gqt-files.s3.amazonaws.com/1kg.phase3.ped.db"]
        prefix = '/home/ec2-user/environment/python-gqt/'
        #prefix = ''
        res = ['./lib/gqt/bin/gqt', 'query', "-d", "http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db"]
        
        
        
        
        '''
        f = ''
        
        for i in form: 
            f += i + ' '
        return f
        '''
        both = False
        part = ""
        pop = False
        for item in form:
            if item == "form":
                continue
            elif item in chs:
                index = chs.index(item)
                res.extend(["-i", " http://gqt-files.s3.amazonaws.com/" + files[index]])
            elif item == "-p":
                #if not len(res) == 6:
                    #part += ')"'
                    #res.append(part)
                part = ""
                res.append("-p")
                continue
            elif item == "Gender":
                both = False
                part += '"Gender = '
                continue
            elif item == "Male":
                part += '1" '
                res.append(part)
                part = ''
                continue
            elif item == "Female":
                part += '2" '
                res.append(part)
                part = ''
                continue
            elif item == "Population":
                both = False
                pop = True
                part += '"Population in ('
            elif (item in ['CHS', 'GBR', 'PUR', 'CLM', 'MXL', 'TSI', 'LWK', 'JPT', 'IBS', 'PEL', 'CDX', 'YRI', 'KHV', 'ASW', 'ACB', 'CHB', 'GIH', 'GWD', 'PJL', 'MSL', 'BEB', 'ESN', 'STU', 'ITU']):
                if both:
                    'and Population in ('
                    both = False
                part += "'" + item + "'" + ", "
                continue
            elif item == "Both":
                both == True
                part += '"Gender = '
                continue
            elif item == "-g":
                if pop == True:
                    part = part[:-2] + ')"'
                    res.append(part)
                    part = ""
                    pop = False
                part = ''
                res.append("-g")
                continue
            elif item == "Heterozygous":
                part += "HET "
                #res.append("HET ")
                continue
            elif item == "Homozygous":
                continue
            elif item == "Reference":
                part += "HOM_REF "
                #res.append("HOM_REF ")
            elif item == "Alternate":
                #res.append("HOM_ALT ")
                part += "HOM_ALT "
            elif item == "Count":
                part += '"count( '
                #res.append('"count( ')
            elif item == "MAF":
                part += '"maf('
            elif item == "Percent":
                part += '"pct( '
            elif item in ['<','<=','==','>=','>']:
                part += ') ' + item + ' '
            elif item[0].isdecimal() or item[0] == '.':
                res.append(part + item + '"')
                part = ''
            elif item =='-c':
                res.append('-c')
        #res.append(part + ')"')
        
        #return params  
        cmd = ""  
        key = ""
        after_pg = False
        for arg in res:
            if arg == "-p" or arg == "-g":
                key += arg
                after_pg = True
            elif after_pg:
                key += arg
                after_pg = False
            cmd += arg + ' '
        key = key.replace(" ", "")
        key = key.replace("'", "*")
        key = key.replace('"', "*")
        key = key.replace('=', "*")
        key = key.replace('<', "*")
        key = key.replace('>', "*")
        key = '"' + key + '.txt"'
        bucket_name="gqt-results"
        cmd += "| aws s3 cp - s3://" + bucket_name + "/" + key +  " --acl public-read"
        url = 'http://' + bucket_name + '.s3.amazonaws.com/' + key[1:-1]
        num_tries = 0
        while num_tries < 4:
            try:
                proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
                err = proc.communicate()[1]
                if err == "":
                    return render_template("response.html", url=url)
                elif err[-4] == "peer":
                    num_tries += 1
                else:
                    s3_resource = boto3.resource('s3')
                    bucket = s3_resource.Bucket('gqt-results')
                    obj = bucket.put_object(Key=key[1:-1],Body=err, ACL='public-read')
                    return render_template("response.html", url=url)
            except Exception as e:
                
                s3_resource = boto3.resource('s3')
                bucket = s3_resource.Bucket('gqt-results')
                obj = bucket.put_object(Key=key[1:-1],Body=str(e), ACL='public-read')
                return render_template("response.html", url=url)
            
        
        
        
        
        
        
        import gqt
        
        out_file_name = '/tmp/tst_redir.txt'
        f = open(out_file_name, 'w')
        try:
            proc = subprocess.check_call(res,
                                         stderr=None,
                                         stdout=f)
            sys.stderr.write("\n\n\Command: {0}\n\n\n".format(res))
            # res = subprocess.check_output(cmd,stderr=sys.stderr)
            # sys.stderr.write("\n\n\nResult: {0}\n\n\n".format(res))
        except Exception as e:
            return str(e)
        f.close()
        f = open(out_file_name, 'r')
        #return f.read()
        s3_resource = boto3.resource('s3')
        s3_client = boto3.client('s3')
        bucket_name = 'layer-overflow-bucket'
        bucket = s3_resource.Bucket(bucket_name)
        
        key = 'query_test.txt'
        s3_client.upload_file('/tmp/tst_redir.txt', bucket_name, key)
        
        #with open("/tmp/tst_redir.log", 'r') as data:
            #bucket.put_object(Key=key, Body=data
        #obj = bucket.put_object(Key='s3-results',Body=response, ACL='authenticated-read')
        url = s3_client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=120)
        
        '''
        bashCommand = "ls /tmp"
        import subprocess
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        #command = os.popen('ls /tmp')
        #print(output)
        '''
        return url

            

                
                
                
                
        #for fun in funlist:
            
        
        #fun = request.form["Function"].lower()
        '''
        if not (fun == "maf"):
            fun += "("
            if "gen1" in request.form:
                fun += "HOM_REF "
            if "gen2" in request.form:
                fun += "HET "
            if "gen3" in request.form:
                fun += "HOM_ALT"
            fun += ")"
        else:
            fun += "()"
        '''  
        
        
        return '''<h1>{}</h1>'''.format(res)
        
        #return '''<h1>The i value is: {}</h1>
        #          <h1>The d value is: {}</h1>'''.format(i, d)
        

    return render_template("query.html")
              
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=80, debug='on')