class Health:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.current_hp = self.max_hp    

    def take_damage(self, amount):
        self.current_hp -= amount

    def heal_damage(self, amount):
        self.current_hp += amount

    
