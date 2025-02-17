class ParticleContainer:
    def __init__(self):
        self.container = []

    def add(self, particle):
        self.container.append(particle)

    def update(self):
        removeParticleArray = []
        for particle in self.container:
            particle.update()
            if particle.remove:
                removeParticleArray.append(particle)
        for particle in removeParticleArray:
            self.container.remove(particle)

    def draw(self):
        for particle in self.container:
            particle.draw()