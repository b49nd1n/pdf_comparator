from setuptools import setup

setup(
    name='pdf_comparator',
    version='0.1.0',    
    description='PDF-files comparator tool',
    url='https://github.com/b49nd1n/pdf_comparator',
    author='Mike Bayandin',
    author_email='me@b49nd1n.ru',
    license='MIT',
    packages=['pdf_comparator','pdf_comparator.comparators'],
    install_requires=['PyPDF2==3.0.0',
                      'PyMuPDF==1.22.5',
                      'Pillow==9.2.0',
                      'ImageHash==4.3.1'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
