# coding: utf-8
# author: Yikai Ni
# multiprocessing version of pdf to text
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from multiprocessing import Pool, Lock, Process
from glob import glob

pdfdirpath = "../examples"
textdirpath = "../texts"
n_process = 3

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text 

def converter(fname):
    lock.acquire()
    print('... processing ...', fname)
    lock.release()
    txtfname = textdirpath+fname[len(pdfdirpath):-3]+"txt"
    
    try:
        with open(txtfname, "w") as ofile:
            ofile.write(convert(fname))
    except:
        lock.acquire()
        print('!!! error !!!', fname)
        lock.release()

def init(l):
    global lock
    lock = l

if __name__ == '__main__':

    files = glob(pdfdirpath+"/*.pdf")
    lock = Lock()
    pool = Pool(initializer = init, initargs = (lock,), processes = n_process)

    for fname in files:
        result = pool.apply_async(converter, (fname,))
    pool.close()
    pool.join()
