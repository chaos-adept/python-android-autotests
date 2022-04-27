
===
How to run

1. [install](https://docs.docker.com/engine/install/) docker 
2. build docker image
`docker build . -t python-android-autotests`
3. run
`docker run -it python-android-autotests:latest`
it consumes the stdin so the more useful command is the following:
windows
`docker run -i python-android-autotests:latest < src/code_samples/author_solution.java_fragment`
linux
`cat src/samples/author_solution.java_fragment | docker run -i python-android-autotests:latest`

====

Implementation notes

Folder structure notes

* src/main - entry point
* src/samples - samples for tests purposes
* src/codetrainer/data/templates - templates for code generation

Implementation based on the verification java code sample in the several phases

1. pre-check - verification that code has required keywords and variable initialization
1. compilation check - verification that code can be compiled
1. runtime check - verification that code can be exectuted
1. test-cases run - verification that code can pass test cases

based on the student task
- студент не заменил создание массива и цикл на захардкоженный вывод  (pre-check & test-cases)
- код студента корректно работает при разных значениях n (в заготовке нет ввода n) (test-cases)
- используется цикл for (pre-check)
- массив заполняется корректно, то есть значения не вычисляются на лету при выводе (test-cases)

В то же время мы считаем, что студент не будет переименовывать объявленные в коде переменные (pre-check)

====

On-Host Development

1. create venv
`python -m virtualenv --python=python3.9 venv39`
1. activate 
`source venv39/bin/activate`
1. install requirements
`pip install -r requirements.txt`
`pip install -r requirements.testing.txt`
====

the main idea

**Verify the following in the sample code**

- arr is created and filled without the hardcoded values
e.g. System.out.println(1); System.out.println(2);

- code sample works for random n values (code template doesn't have input for n)
- for statements "for" is used
- array items assigned in the "for" (without calc on the fly)

the non strict requirement that student is not going to rename variables from the template

the Code Template
```
int n = 5;
int[] arr = ...; // создайте массив размера n
for (...) { // запишите в arr n квадратов чисел от 1 до n
  ...
}
for (int i = 0; i < n; i++) {
  System.out.println(arr[i]);
}
```

the author solution 
```
int n = 5;
int[] arr = new int[n];
for (int i = 1; i <= n; i++) {
  arr[i] = i * i;
}
for (int i = 0; i < n; i++) {
  System.out.println(arr[i]);
}
```


functional requirements

- add missing code construction for verifying 
- generate correct java-file, which can be compiled and executed
- run a generated class on test-cases, test-cases can be presented as text files or by other suitable forms

Non-functional
- check that it faces limites of memory and time execution