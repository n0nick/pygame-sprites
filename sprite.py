import pygame
from operator import truth


ANCHOR_TOPLEFT = 101
ANCHOR_TOPRIGHT = 102
ANCHOR_BOTTOMLEFT = 103
ANCHOR_BOTTOMRIGHT = 104
ANCHOR_CENTER = 105


class Sprite(object):
    """simple base class for visible game objects

    pygame.sprite.Sprite(*groups): return Sprite

    The base class for visible game objects. Derived classes will want to
    override the Sprite.update() method and assign Sprite.image and Sprite.rect
    attributes.  The initializer can accept any number of Group instances that
    the Sprite will become a member of.

    When subclassing the Sprite class, be sure to call the base initializer
    before adding the Sprite to Groups.

    """

    def __init__(self, *groups):
        self.image = None
        self.rect = None

        self.anchor = ANCHOR_TOPLEFT
        self.position = None

        # visual attributes
        self.scale = 1
        self.rotate = 0

        self.__g = {}  # The groups the sprite is in
        if groups:
            self.add(*groups)

    @property
    def image(self):
        try:
            img = self._image
        except AttributeError:
            img = None

        if img is not None:
            if self.scale != 1 or self.rotate != 0:
                if self.scale != 1:
                    img = pygame.transform.scale(img, self.scaled_size())
                if self.rotate != 0:
                    img = pygame.transform.rotate(img, self.rotate)
                self.rect = img.get_rect()
                self.position = self.position

        return img

    @image.setter
    def image(self, img):
        self._image = img

    #TODO handle negative values
    #TODO use same constants as Rect's
    def anchor_value(self):
        if type(self.anchor) is tuple:
            return self.anchor
        elif self.anchor == ANCHOR_TOPLEFT:
            return (0, 0)
        elif self.anchor == ANCHOR_TOPRIGHT:
            return (self.rect.width, 0)
        elif self.anchor == ANCHOR_BOTTOMLEFT:
            return (0, self.rect.height)
        elif self.anchor == ANCHOR_BOTTOMRIGHT:
            return (self.rect.width, self.rect.height)
        elif self.anchor == ANCHOR_CENTER:
            return (self.rect.width / 2, self.rect.height / 2)
        else:
            return None  # shouldn't happen :(

    @property
    def position(self):
        return self._position

    #TODO handle float values
    @position.setter
    def position(self, value):
        self._position = value
        if value:
            anchor = self.anchor_value()
            x = value[0] - anchor[0]
            y = value[1] - anchor[1]
            self.rect.topleft = (x, y)

    @property
    def scale(self):
        try:
            return self._scale
        except AttributeError:
            return 1

    @scale.setter
    def scale(self, ratio):
        if ratio < 0:
            raise AttributeError("ratio must be a positive float")
        self._scale = ratio

    def scaled_size(self):
        (width, height) = self._image.get_size()
        width = (int)(width * self.scale)
        height = (int)(height * self.scale)
        return (width, height)

    @property
    def rotate(self):
        try:
            return self._rotate
        except AttributeError:
            return 0

    @rotate.setter
    def rotate(self, degree):
        self._rotate = degree % 360  # TODO magic number?

    def add(self, *groups):
        """add the sprite to groups

        Sprite.add(*groups): return None

        Any number of Group instances can be passed as arguments. The
        Sprite will be added to the Groups it is not already a member of.

        """
        has = self.__g.__contains__
        for group in groups:
            if hasattr(group, '_spritegroup'):
                if not has(group):
                    group.add_internal(self)
                    self.add_internal(group)
            else:
                self.add(*group)

    def remove(self, *groups):
        """remove the sprite from groups

        Sprite.remove(*groups): return None

        Any number of Group instances can be passed as arguments. The Sprite
        will be removed from the Groups it is currently a member of.

        """
        has = self.__g.__contains__
        for group in groups:
            if hasattr(group, '_spritegroup'):
                if has(group):
                    group.remove_internal(self)
                    self.remove_internal(group)
            else:
                self.remove(*group)

    def add_internal(self, group):
        self.__g[group] = 0

    def remove_internal(self, group):
        del self.__g[group]

    def update(self, *args):
        """method to control sprite behavior

        Sprite.update(*args):

        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        Group.update() with whatever arguments you give it.

        There is no need to use this method if not using the convenience
        method by the same name in the Group class.

        """
        pass

    def kill(self):
        """remove the Sprite from all Groups

        Sprite.kill(): return None

        The Sprite is removed from all the Groups that contain it. This won't
        change anything about the state of the Sprite. It is possible to
        continue to use the Sprite after this method has been called, including
        adding it to Groups.

        """
        for c in self.__g:
            c.remove_internal(self)
        self.__g.clear()

    def groups(self):
        """list of Groups that contain this Sprite

        Sprite.groups(): return group_list

        Returns a list of all the Groups that contain this Sprite.

        """
        return list(self.__g)

    def alive(self):
        """does the sprite belong to any groups

        Sprite.alive(): return bool

        Returns True when the Sprite belongs to one or more Groups.
        """
        return truth(self.__g)

    def __repr__(self):
        return "<%s sprite(in %d groups)>" \
                % (self.__class__.__name__, len(self.__g))
