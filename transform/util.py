def apply_to_first_col(fn):
    def inner(df,*args,**kwargs):
        df[df.columns[0]] = fn(df[df.columns[0]],*args,**kwargs)
        return df
    return inner
