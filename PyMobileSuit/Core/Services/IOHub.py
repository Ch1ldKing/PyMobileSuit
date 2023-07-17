class PureTextIOHub(IOHub):
    """IO hub with pure text output."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOhub."""
        super().__init__(promptFormatter, configurator)

    def Write(self, content: PrintUnit) -> None:
        """Write content to the output stream."""
        self.Output.write(content.Text)

    async def WriteAsync(self, content: PrintUnit) -> None:
        """Write content to the output stream asynchronously."""
        await self.Output.write(content.Text)

class IOHub4Bit(IOHub):
    """IO hub using 4-bit color output."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOhub."""
        super().__init__(promptFormatter, configurator)

    @staticmethod
    def BackgroundCodeOf(c: Color) -> int:
        return 10 + IOHub4Bit.ForegroundCodeOf(c)

    @staticmethod
    def ForegroundCodeOf(c: Color) -> int:
        return {
            ConsoleColor.Black: 30,
            ConsoleColor.DarkBlue: 34,
            ConsoleColor.DarkGreen: 32,
            ConsoleColor.DarkCyan: 36,
            ConsoleColor.DarkRed: 31,
            ConsoleColor.DarkMagenta: 35,
            ConsoleColor.DarkYellow: 33,
            ConsoleColor.Gray: 90,
            ConsoleColor.DarkGray: 37,
            ConsoleColor.Blue: 94,
            ConsoleColor.Green: 92,
            ConsoleColor.Cyan: 96,
            ConsoleColor.Red: 91,
            ConsoleColor.Magenta: 95,
            ConsoleColor.Yellow: 93,
            ConsoleColor.White: 97
        }[IOHub4Bit.ConsoleColorOf(c)]

    @staticmethod
    def ConsoleColorOf(color: Color) -> ConsoleColor:
        r, g, b = color.R, color.G, color.B
        delta = float("inf")
        re = None
        for cc in ConsoleColor:
            c = PrintUnit.ConsoleColorCast(cc)
            t = (c.R - r) ** 2 + (c.G - g) ** 2 + (c.B - b) ** 2
            if t == 0:
                return cc
            if t < delta:
                delta = t
                re = cc
        return re

    def Write(self, content: PrintUnit) -> None:
        """Write content to the output stream."""
        if content.Foreground is not None:
            f = content.Foreground
            self.Output.write(f"\u001b[{self.ForegroundCodeOf(f)}m")
        if content.Background is not None:
            b = content.Background
            self.Output.write(f"\u001b[{self.BackgroundCodeOf(b)}m")
        self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            self.Output.write("\u001b[0m")

    async def WriteAsync(self, content: PrintUnit) -> None:
        """Write content to the output stream asynchronously."""
        if content.Foreground is not None:
            f = content.Foreground
            await self.Output.write(f"\u001b[{self.ForegroundCodeOf(f)}m")
        if content.Background is not None:
            b = content.Background
            await self.Output.write(f"\u001b[{self.BackgroundCodeOf(b)}m")
        await self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            await self.Output.write("\u001b[0m")

class IOHub(IIOHub):
    """A entity, which serves the input/output of a mobile suit."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOServer."""
        self.ColorSetting = IColorSetting.DefaultColorSetting
        self.Input = sys.stdin
        self.Output = sys.stdout
        self.ErrorStream = sys.stderr
        self.FormatPrompt = promptFormatter
        configurator(self)
        self.Prefix = []

    @property
    def ColorSetting(self) -> IColorSetting:
        return self._ColorSetting

    @ColorSetting.setter
    def ColorSetting(self, value: IColorSetting) -> None:
        self._ColorSetting = value

    @property
    def FormatPrompt(self) -> PromptFormatter:
        return self._FormatPrompt

    @FormatPrompt.setter
    def FormatPrompt(self, value: PromptFormatter) -> None:
        self._FormatPrompt = value

    def Write(self, content: PrintUnit) -> None:
        """Write content to the output stream."""
        raise NotImplementedError()

    async def WriteAsync(self, content: PrintUnit) -> None:
        """Write content to the output stream asynchronously."""
        raise NotImplementedError()
