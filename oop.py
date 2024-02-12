from typing import Any


class Human:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"hello {self.name}")

    def woof(self):
        print("woof")


# inheritance -> 반복적인 부분을 추상화할 수 있다.
class Player(Human):
    def __init__(self, name, age):  # self = class를 가리킨다.
        super().__init__(name)  # 부모 클래스의 init(생성자) 메서드를 호출
        self.age = age

    def woof(self):
        super().woof()  # 이름을 직접 적지 않고 부모 클래스에 접근할 수 있다. 가장 먼저 상속받는 클래스에 접근 -> 다중 상속 = 클래스 이름 명시해 접근
        print("Hi")


class Fan(Human):
    def __init__(self, name, fev_team):
        super().__init__(name)
        self.fev_team = fev_team

    # 부모 클래스에 있는 메소드를 자식 클래스만의 메소드로 가지고 싶을 때 -> 오버라이딩
    def woof(self):
        print(f"{self.name}'s fan")


zzone = Player("zzone", 5)
zzone.woof()
zzone.say_hello()
print("\n")
zzone_fan = Fan("zzone_fan", "ddeock")
zzone_fan.woof()
zzone_fan.say_hello()


class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "zzoneddeock!!"

    def __getattribute__(self, name):
        print(f"they want to get {name}")
        return "🐈"


jia = Dog("jia")
print(jia)
print(dir(jia))
print(jia.name)
# 메모리 주소값 -> 클래스가 문자열로 보이는 방식을 커스텀할 수 있다. => 매직 메소드
