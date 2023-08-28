## lateraligator\_text\_tool

later aligator 텍스트 교체 툴.

main.py를 텍스트 에디터로 연 후, 아래 부분을 원하는 대로 변경한 다음 실행.

> if \_\_name\_\_ == "\_\_main\_\_":
> 
>     extract\_bundles()
> 
>     # import\_bundles()
> 
>     # extract\_test("./2.edited\_bundle/scenes\_scenes\_artdealer.bundle")
> 
>     # extract\_test("./2.edited\_bundle/scenes\_scenes\_grilldad.bundle")
> 
>     # extract\_test("./2.edited\_bundle/scenes\_scenes\_locationintro.bundle")
> 
>     pass

*   extract\_bundles() - \[1.original\_bundle\] 폴더 내 .bundle 파일들을 읽어, “storyText” 필드를 긁어와 CSV 파일로 저장합니다. (optional parameter - 저장될 CSV 이름)
*   import\_bundles() - CSV 파일의 filename, itemid를 고유한 값으로 하여 텍스트를 번역된 텍스트로 교체하고, 수정된 .bundle 파일을 \[2.edited\_bundle\]에 저장합니다. (optional parameter - 불러올 CSV 이름)
*   extract\_test() - 특정 번들에 대해서만 extract 작업을 진행하고, 결과를 번들 이름과 동일한 이름의 CSV에 저장합니다.