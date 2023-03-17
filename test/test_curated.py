from rich.pretty import pprint


def test_curated_files(curated_pair, grammar, record_property):
    rule, src = curated_pair
    src_text = src.read_text("utf-8")
    out = grammar.parse(
        src_text,
        start=rule,
        trace=True,
        trace_filename=True,
        trace_length=9999,
        parseinfo=True,
    )

    pprint(out)


def test_curated_variable(variable_line, grammar):
    """Pass or fail, wants a declaration with or without assignment"""
    print("\n")
    print(f"{variable_line=}")
    out = grammar.parse(variable_line, start="one_decl", trace=True)
    pprint(out)


s = """\
class NumberSelector
{
    public Number Value;

    Any numberText;
    Any decrementText;
    Any incrementText;

    public constructor(in Number initialValue, in Number posX, in Number posY, in Boolean visible)
    {
        Value = initialValue;
        numberText = createButton(
            ' {0} '.Format([initialValue]),
            scale: 2.5,
            posX: posX,
            posY: posY,
            defaultColor: Color.Yellow,
            interactable: false,
            visible: visible);
        incrementText = createButton(
            '→',
            primaryAction: [MenuAction.AttributeIncrement, this],
            secondaryAction: [MenuAction.AttributeIncrementBig, this],
            scale: 4,
            posX: posX + 0.1775,
            posY: posY,
            visible: visible);
        decrementText = createButton(
            '←',
            primaryAction: [MenuAction.AttributeDecrement, this],
            secondaryAction: [MenuAction.AttributeDecrementBig, this],
            scale: 4,
            posX: posX - 0.1775,
            posY: posY,
            visible: visible);

        this.onUpdate = onUpdate;
    }

    void SetVisible(in Boolean visible)
    {
        SetVisible(numberText, visible);
        SetVisible(incrementText, visible);
        SetVisible(decrementText, visible);
    }

    public void Add(in Number amount)
    {
        Value += amount;
        Update();
    }

    public void Set(in Number value)
    {
        Value = value;
        Update();
    }

    void Update()
    {
        SetLabel(numberText, ' {0} '.Format([Value]));
        onUpdate(Value);
    }

    public void Dispose()
    {
        DestroyButton(numberText);
        DestroyButton(incrementText);
        DestroyButton(decrementText);
        delete this;
    }
}
"""


def test_expr(grammar):
    sample = "    public constructor(in Number.Potato initialValue, in Number posX, in Number posY, in Boolean visible)"

    sample = "{Value = initialValue;}"
    # sample = s
    out = grammar.parse(sample, start="class_body", trace=True, trace_filename=True)
    print("\n")

    pprint(sample)
    pprint(out)
