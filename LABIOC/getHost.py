
class ColorTest(object):
    color = "color"
    @classmethod
    def value(self):
        return self.color
     
class Red(ColorTest):
    color = "red"
     
class Green(ColorTest):
    color = "green"
 
g = Green()
print(g.value())
print(Green.value())
