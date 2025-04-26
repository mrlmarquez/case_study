from case_study.graphs.irac import IRACGraph


def main():
    inputs = {
        "active_clause": """DURATION OF TERM:
A.
The Primary Term and duration of the Lease shall be for a period of 5 years, commencing the 1" day of April, 2006
(the "Commencement Date").
B.
Provided the TENANT has not defaulted under the terms of this Lease, the TENANT shall have the right, privilege
and option of extending this Lease for an additional period of 5 years (hereinafter referred to as Secondary Term) commencing
upon the termination date of the Primary Term set forth above.
The TENANT shall exercise its option for the Secondary Term of
this Lease by delivering written notice to the LANDLORD at least 180 days prior to, and no more than 210 days prior to, the
expiration of the Primary Term by Certified Mail.""",
        "incoming_clause": """DURATION OF TERM:
A.
The Primary Term and duration of the Lease shall be for a period of 15 years, commencing the 2nd day of April, 2011
(the "Commencement Date").
B.
Provided the TENANT has not defaulted under the terms of this Lease, the TENANT shall have the right, privilege
and option of extending this Lease for an additional period of 15 years (hereinafter referred to as Secondary Term) commencing
upon the termination date of the Primary Term set forth above.
The TENANT shall exercise its option for the Secondary Term of
this Lease by delivering written notice to the LANDLORD at least 180 days prior to, and no more than 210 days prior to, the
expiration of the Primary Term by Certified Mail.""",
        "max_retries": 3,
    }
    irac = IRACGraph()
    print(irac)
    for event in irac.graph.stream(inputs, stream_mode="values"):
        print(event)


if __name__ == "__main__":
    main()
