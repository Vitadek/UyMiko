#!/usr/bin/env python3
from __future__ import annotations
import pytermgui as ptg
import netmiko as nko
import time


def define_slow_macro(
    ms_per_char: int = 50, lang: ptg.MarkupLanguage = ptg.tim
) -> str:
    start = time.time()
    def _macro(text: str) -> str:
        current = time.time()
        char_count = (current - start) / (ms_per_char / 1000)

        trimmed = text[: round(char_count)]

        if int(current) % 2 == 0:
            return trimmed + "█"

        return trimmed

    name = f"!slow{str(time.time())[-5:]}"
    lang.define(name, _macro)
    return name

def define_fast_macro(
    ms_per_char: int = 30, lang: ptg.MarkupLanguage = ptg.tim
) -> str:
    """Defines a slow typer macro, returns its name.
    Args:
        ms_per_char: How many milliseconds should pass between each
            char being displayed.
        lang: The markup language to define the new macro on.
    Returns:
        The name of the newly defined macro. The name follows the form:
            `slow12345`
        ...where `12345` is the last 5 characters of the current `time.time()`.
    """
    start = time.time()
    def _macro(text: str) -> str:
        current = time.time()
        char_count = (current - start) / (ms_per_char / 1000)

        trimmed = text[: round(char_count)]

        if int(current) % 2 == 0:
            return trimmed + "█"

        return trimmed

    name = f"!fast{str(time.time())[-5:]}"
    lang.define(name, _macro)
    return name


CONNECTION = {
    "device_type": "cisco_ios",
    "ip": "1.1.1.1",
    "username": "some_username",
    "password": "some_password",
    "name": "some connection"
}


def update_connection(command: str, field: str) -> any:
    cm_st = {command: field}
    CONNECTION.update(cm_st)


def input_box(title: str, command: str) -> ptg.Container:
    """Create a Container with title, containing an InputField"""

    box = ptg.Container()
    box.set_char("corner", ["x- " + title + " -", "x", "x", "x"])
    box.set_char("border", ["| ", "-", " |", "-"])
    field = ptg.InputField()
    field.bind(ptg.keys.RETURN, lambda field, _: update_connection(command, field.value))
    box += field
    return box


# def somesplitter()


def execute_all(window: ptg.Window) -> None:
    """Execute all `RETURN` bindings in window"""

    for field, _ in window.selectables:
         if not isinstance(field, ptg.InputField):
             continue

         field.execute_binding(ptg.keys.RETURN)
    window.close()
    isnext()

def goto_main(window: ptg.Window):
    window.close()
    main()

def main() -> None:
    """Main method"""
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(width=100)
            + ""
            + ptg.Label(
                "[240 italic]> Press RETURN to run each command", parent_align=0
            )
            + ""
            + input_box("Edit Connection Name", "name")
            + input_box("Edit IP", "ip")
            + input_box("Edit Username", "username")
            + input_box("Edit Password", "password")
            + ptg.Button("Submit all!", lambda *_: execute_all(window))
            # + ptg.Button("Close", lambda end: window.close())
        ).center()
        manager.add(window)
        manager.run()

def next_onto(window: ptg.Window):
    window.close()
    mmain()

def isnext() -> None:
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(width=100)
            + ptg.Label(CONNECTION["name"])
            + ptg.Label(CONNECTION["ip"])
            + ptg.Label(CONNECTION["username"])
            + ptg.Label(CONNECTION["password"])
            +""
            + ptg.Button("Edit", lambda edit: goto_main(window))
            + ptg.Button("Close", lambda end: next_onto(window))
        ).center()
        manager.add(window)
        manager.run()

def query(cmnds: str, window: ptg.Window) -> None: #this function returns a dictionary
    window.close()
    definitions = {
        "show running config": "This displays the entire running config. Or the config that is currently being used. If the commmand: \"copy run start\" (the command: \"write\" also works), is used - then the changes from running config will be applied to starting config",
        "show ip interface brief": "This displays the interfaces and their status",
        "show run | include ip route": "This displays the current static ip route configuration. Not to be confused by \"show ip route\" - which is the ip routes that have been manually configured, connected, or discovered by routing protocols i.e. OSPF, BGP, EIGRP, etc...",
        "show ip ospf neighbor brief": "This displays active OSPFv2 neighborships - OSPFv2 meaning the interface that is advertising routes are advertised as IPv4 (as OSPFv2 only supports IPv4)",
        "show ospf neighbor brief": "This displays active OSPFv3 neighborships - OSPFv3 meaning the interface that is advertising routes are advertised as IPv6 (OSPFv3 is the only OSPF ver that supports IPv6)",
        "clear crypto ikev2 sa": "This clears all sa's (or security associations), generally this is used to clear a bad security association or a stuck association *hint* this is for VPN connections",
        "show crypto ikev2 client flexvpn": "This shows flexvpn current status - meaning the target peer status for SA's (Security Associations).",
        "show run | section flexvpn": "This shows the flexvpn configuration - it'll show the configured target peers for SA's (Security Associations)",
    }
    with ptg.WindowManager() as manager:
        fast1 = define_fast_macro()
        time.sleep(0.1)
        window = (
            ptg.Window(width=100, height=5)
            + ptg.Label(f"[{fast1}]" + definitions[cmnds])
            + ptg.Button("Close", lambda _: next_onto(window))
        ).center()
        manager.add(window)
        manager.run()

    # return definitions[cmnds]

def send_command(cmnds: str) -> None:
    # net_connect = nko.ConnectHandler(**CONNECTION)
    # net_connect.send_command(cmnds)
    with ptg.WindowManager() as manager:
        slow1 = define_slow_macro()
        time.sleep(0.1)

        window = (
            ptg.Window(width=100)
            + ptg.Label(f"[210 bold {slow1}]" + cmnds)
            + ptg.Button("Send it!", lambda _: next_onto(window))
            + ptg.Button("Go back", lambda _: next_onto(window))
            + ptg.Button("What is this?", lambda _: query(cmnds, window))
        ).center()
        manager.add(window)
        manager.run()

def more_show(window: ptg.Window) -> None:
    window.close()
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(width=100)
            + ptg.Label("More show commands...")
            + (
                ptg.Button("running config", lambda _: send_command("show running config")),
                ptg.Button("ip interfaces", lambda _: send_command("show ip interface brief")),
                ptg.Button("ip routes", lambda _: send_command("show run | include ip route")),
            )
            + (
                ptg.Button("crypto ikev2 client", lambda _: send_command("show crypto ikev2 client flexvpn")),
                ptg.Button(("flexvpn config"), lambda _: send_command("show run | section flexvpn"))

            )
            + ptg.Button("Go back...", lambda _: next_onto(window))
        ).center()
        manager.add(window)
        manager.run()

def manual_mode(command: str) -> None:
    # net_connect = nko.ConnectHandler(**CONNECTION)
    # output = net_connect.send_command(command)
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(width=100,height=10)
            + ptg.Label("Command entered: " + command)
            + ""
            + ptg.Label("Change this string to var output")
            + ptg.Button("Close", lambda _: next_onto(window))
        ).center()
        manager.add(window)
        manager.run()


def mmain() -> None:
    with ptg.WindowManager() as manager:
        manual_config = ptg.InputField()
        manual_config.bind(ptg.keys.RETURN, lambda manual_config, _: manual_mode(manual_config.value))
        window = (
            ptg.Window(width=100)
            +""
            + (
                ptg.Label("\"" + CONNECTION["name"] + "\""),
                ptg.Button("Edit", lambda _: goto_main(window))
            )
            + (
                ptg.Label("show"),
                ptg.Button("os ne br", lambda _: send_command("show ospf neighbor brief")),
                ptg.Button("ip os ne br", lambda _: send_command("show ip ospf neighbor brief")),
                ptg.Button("More show commands", lambda _: more_show(window))
            )
            + (
                ptg.Label("clear->"),
                ptg.Button("Something"),
                ptg.Button("crypto ikev2 sa", lambda _: send_command("clear crypto ikev2 sa"))
            )
            +""
            + (
                ptg.Label("Manual Commands[press enter to send]->"),
                manual_config
            )
        ).center()
        manager.add(window)
        manager.run()






if __name__ == "__main__":
     mmain()
     isnext()
     main()
