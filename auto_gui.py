try: from tkinter import *
except ImportError: from Tkinter import *

#takes a python object, displays a ui for modification, then returns the modified object
def auto_gui(python_object, name=''):
    def text_edit(name,default,root):
        f = Frame(root); f.pack()
        l = Label(f,text=name)
        l.pack(side=LEFT)
        s = StringVar(root); s.set(default)
        t = Entry(f,textvariable=s)
        t.pack(side=RIGHT)
        return s.get

    def compose(f,g):
        def ret():
            return f(g())
        return ret

    def float_edit(name,default,root):
        n = text_edit(name,str(default),root)
        return compose(float,n)

    def bool_edit(name,default,root):
        b = BooleanVar(); b.set(default)
        c = Checkbutton(root,text=name,variable=b)
        c.pack()
        return b.get

    def list_edit(name,default,root):
        n = Label(root,text=name); n.pack()
        f = Frame(root); f.pack()
        l = [generic_edit('',e,f) for i,e in enumerate(default)]
        return lambda : [f() for f in l]

    def dict_edit(name,default,root):
        print(root)
        n = Label(root,text=name); n.pack()
        f = Frame(root); f.pack()
        di = { key:generic_edit(key,default[key],f) for key in sorted(default) }
        return lambda : { key:di[key]() for key in di }

    def generic_edit(name,default,root):
        try:    unicode
        except: unicode = str
        d = {
            list:list_edit,
            float:float_edit,
            int:float_edit,
            bool:bool_edit,
            str:text_edit,
            unicode:text_edit,
            dict:dict_edit,
        }
        t = type(default)
        return d[t](name,default,root)

    r = Tk(); r.wm_title(name)
    ret = {};

    ret["g"] = generic_edit(name,python_object,r)

    b = Button(r,text='return',command=r.destroy); b.pack()
    def revert():
        ret["g"] = lambda : None
        r.destroy()
    r.protocol("WM_DELETE_WINDOW", revert)
    mainloop()
    return ret["g"]()

if __name__ == '__main__':
    import json
    fname = "test.json"
    with open(fname) as f:
        d = json.load(f)
    print(auto_gui(d,fname))
