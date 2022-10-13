from IPython.display import HTML


def video(src):
    return HTML(
        '<iframe width="100%" height="720" src="{}" frameborder="0" allowfullscreen></iframe>'.format(src)
    )