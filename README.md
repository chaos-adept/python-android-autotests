This a test task for praktikum.

The main idea is a automation process of students code samples verification java/kotlin sources.
a student sends code sample "verification tool" applies several checks and returns results.

because it is a test task there is a particular case which needs to be tested


the student task requirements

**Verify the following in the sample code**

- arr is created and filled without the hardcoded values
e.q. System.out.println(1); System.out.println(2);

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


- check that it faces limites of memory and time execution?


- cool feature index diff with author solution?